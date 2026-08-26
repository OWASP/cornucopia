import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import scripts.verify_checkout as checkout


def completed_process(returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["git"], returncode, stdout, stderr)


class VerifyCheckoutTests(unittest.TestCase):
    def test_run_git_uses_repository_root(self) -> None:
        with patch("scripts.verify_checkout.subprocess.run", return_value=completed_process()) as run:
            checkout.run_git("lfs", "version")

        run.assert_called_once_with(
            ["git", "lfs", "version"],
            cwd=checkout.REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_verify_lfs_reports_missing_git_lfs(self) -> None:
        with patch("scripts.verify_checkout.run_git", return_value=completed_process(1)):
            errors = checkout.verify_lfs()

        self.assertEqual(errors, ["Git LFS is not available. Install it from https://git-lfs.com/ and run 'git lfs install'."])

    def test_verify_lfs_reports_list_failure(self) -> None:
        with patch(
            "scripts.verify_checkout.run_git",
            side_effect=[completed_process(), completed_process(1, stderr="list failed")],
        ):
            errors = checkout.verify_lfs()

        self.assertEqual(errors, ["Could not list Git LFS files: list failed"])

    def test_verify_lfs_reports_unhydrated_missing_and_integrity_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository_root = Path(temporary_directory)
            (repository_root / "hydrated.bin").write_bytes(b"binary content")
            (repository_root / "pointer.bin").write_bytes(checkout.LFS_POINTER_PREFIX)

            with (
                patch("scripts.verify_checkout.REPOSITORY_ROOT", repository_root),
                patch(
                    "scripts.verify_checkout.run_git",
                    side_effect=[
                        completed_process(),
                        completed_process(stdout="hydrated.bin\npointer.bin\nmissing.bin\n"),
                        completed_process(1, stdout="integrity failed"),
                    ],
                ),
            ):
                errors = checkout.verify_lfs()

        self.assertEqual(
            errors,
            [
                "Git LFS pointer was not hydrated: pointer.bin",
                "Git LFS file is missing: missing.bin",
                "Git LFS integrity check failed: integrity failed",
            ],
        )

    def test_verify_lfs_reports_integrity_stderr(self) -> None:
        with patch(
            "scripts.verify_checkout.run_git",
            side_effect=[
                completed_process(),
                completed_process(),
                completed_process(1, stderr="integrity failed"),
            ],
        ):
            errors = checkout.verify_lfs()

        self.assertEqual(errors, ["Git LFS integrity check failed: integrity failed"])

    def test_verify_executable_modes_reports_invalid_index_entries(self) -> None:
        with patch("scripts.verify_checkout.REQUIRED_EXECUTABLES", ("failed", "wrong-mode")):
            with patch(
                "scripts.verify_checkout.run_git",
                side_effect=[completed_process(1), completed_process(stdout="100644 hash 0\twrong-mode")],
            ):
                errors = checkout.verify_executable_modes()

        self.assertEqual(
            errors,
            [
                "Git index does not mark this file executable: failed",
                "Git index does not mark this file executable: wrong-mode",
            ],
        )

    def test_verify_executable_modes_checks_posix_checkout_mode(self) -> None:
        file_modes = {
            "executable": stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR,
            "non-executable": stat.S_IRUSR | stat.S_IWUSR,
        }

        with (
            patch("scripts.verify_checkout.REPOSITORY_ROOT", Path("repository")),
            patch("scripts.verify_checkout.REQUIRED_EXECUTABLES", ("executable", "non-executable")),
            patch("scripts.verify_checkout.os.name", "posix"),
            patch(
                "scripts.verify_checkout.Path.stat",
                side_effect=[
                    SimpleNamespace(st_mode=file_modes["executable"]),
                    SimpleNamespace(st_mode=file_modes["non-executable"]),
                ],
            ),
            patch("scripts.verify_checkout.run_git", return_value=completed_process(stdout="100755 hash 0\tfile")),
        ):
            errors = checkout.verify_executable_modes()

        self.assertEqual(errors, ["Checkout does not mark this file executable: non-executable"])

    def test_verify_executable_modes_skips_filesystem_mode_on_windows(self) -> None:
        with (
            patch("scripts.verify_checkout.REQUIRED_EXECUTABLES", ("script.bat",)),
            patch("scripts.verify_checkout.os.name", "nt"),
            patch("scripts.verify_checkout.run_git", return_value=completed_process(stdout="100755 hash 0\tscript.bat")),
        ):
            errors = checkout.verify_executable_modes()

        self.assertEqual(errors, [])

    def test_main_reports_success(self) -> None:
        output = io.StringIO()
        with (
            patch("scripts.verify_checkout.verify_lfs", return_value=[]),
            patch("scripts.verify_checkout.verify_executable_modes", return_value=[]),
            redirect_stdout(output),
        ):
            result = checkout.main()

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "Repository checkout verification passed.\n")

    def test_main_reports_failures(self) -> None:
        output = io.StringIO()
        with (
            patch("scripts.verify_checkout.verify_lfs", return_value=["LFS failure"]),
            patch("scripts.verify_checkout.verify_executable_modes", return_value=["mode failure"]),
            redirect_stderr(output),
        ):
            result = checkout.main()

        self.assertEqual(result, 1)
        self.assertEqual(
            output.getvalue(),
            "Repository checkout verification failed:\n"
            "- LFS failure\n"
            "- mode failure\n"
            "Run 'git lfs pull' and 'git lfs checkout', then retry.\n",
        )