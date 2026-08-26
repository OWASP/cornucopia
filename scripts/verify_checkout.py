"""Verify that a checkout has hydrated Git LFS files and required script modes."""

import os
from pathlib import Path
import stat
import subprocess
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1\n"
REQUIRED_EXECUTABLES = (
    ".clusterfuzzlite/build.sh",
    "copi.owasp.org/rel/env.sh.eex",
    "copi.owasp.org/rel/overlays/bin/migrate",
    "copi.owasp.org/rel/overlays/bin/server",
    "copi.owasp.org/rel/overlays/bin/migrate.bat",
    "copi.owasp.org/rel/overlays/bin/server.bat",
)


def run_git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def verify_lfs() -> list[str]:
    errors: list[str] = []
    version = run_git("lfs", "version")
    if version.returncode != 0:
        return ["Git LFS is not available. Install it from https://git-lfs.com/ and run 'git lfs install'."]

    lfs_files = run_git("lfs", "ls-files", "--name-only")
    if lfs_files.returncode != 0:
        return [f"Could not list Git LFS files: {lfs_files.stderr.strip()}"]

    for relative_path in filter(None, lfs_files.stdout.splitlines()):
        file_path = REPOSITORY_ROOT / relative_path
        try:
            with file_path.open("rb") as file:
                if file.read(len(LFS_POINTER_PREFIX)) == LFS_POINTER_PREFIX:
                    errors.append(f"Git LFS pointer was not hydrated: {relative_path}")
        except FileNotFoundError:
            errors.append(f"Git LFS file is missing: {relative_path}")

    integrity = run_git("lfs", "fsck")
    if integrity.returncode != 0:
        errors.append(f"Git LFS integrity check failed: {integrity.stderr.strip() or integrity.stdout.strip()}")

    return errors


def verify_executable_modes() -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_EXECUTABLES:
        index_entry = run_git("ls-files", "--stage", "--", relative_path)
        if index_entry.returncode != 0 or not index_entry.stdout.startswith("100755 "):
            errors.append(f"Git index does not mark this file executable: {relative_path}")
            continue

        if os.name != "nt" and not (REPOSITORY_ROOT / relative_path).stat().st_mode & stat.S_IXUSR:
            errors.append(f"Checkout does not mark this file executable: {relative_path}")
    return errors


def main() -> int:
    errors = verify_lfs() + verify_executable_modes()
    if errors:
        print("Repository checkout verification failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print("Run 'git lfs pull' and 'git lfs checkout', then retry.", file=sys.stderr)
        return 1

    print("Repository checkout verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())