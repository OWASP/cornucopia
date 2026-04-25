import unittest
import unittest.mock as mock
import argparse
import os
import tempfile
import subprocess
import xml.etree.ElementTree as ET

import scripts.convert as c

c.convert_vars = c.ConvertVars()
c.convert_vars.BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(c.__file__)))[0]


class TestValidateFilePaths(unittest.TestCase):
    """Tests for _validate_file_paths security validation."""

    def test_source_file_does_not_exist(self) -> None:
        """Should return False when source file does not exist."""
        result = c._validate_file_paths("nonexistent_file.odt", "output/test.pdf")
        self.assertFalse(result[0])
        self.assertIn("does not exist", result[1])

    def test_output_directory_does_not_exist(self) -> None:
        """Should return False when output directory does not exist."""
        with tempfile.NamedTemporaryFile(suffix=".odt", delete=False) as f:
            tmp = f.name
        try:
            result = c._validate_file_paths(tmp, "/nonexistent_dir_xyz/test.pdf")
            self.assertFalse(result[0])
            self.assertIn("does not exist", result[1])
        finally:
            os.unlink(tmp)

    def test_source_path_outside_base_directory(self) -> None:
        """Should return False when source path is outside BASE_PATH (path traversal prevention)."""
        with tempfile.NamedTemporaryFile(suffix=".odt", delete=False, dir=tempfile.gettempdir()) as f:
            tmp = f.name
        out_dir = os.path.join(c.convert_vars.BASE_PATH, "output")
        os.makedirs(out_dir, exist_ok=True)
        try:
            result = c._validate_file_paths(tmp, os.path.join(out_dir, "test.pdf"))
            self.assertFalse(result[0])
            self.assertIn("outside base directory", result[1])
        finally:
            os.unlink(tmp)

    def test_valid_paths_returns_true(self) -> None:
        """Should return True when source exists and both paths are within BASE_PATH."""
        src = os.path.join(
            c.convert_vars.BASE_PATH, "resources", "templates", "owasp_cornucopia_webapp_ver_guide_bridge_en.odt"
        )
        out_dir = os.path.join(c.convert_vars.BASE_PATH, "output")
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "test.pdf")
        if os.path.exists(src):
            result = c._validate_file_paths(src, out)
            self.assertTrue(result[0])
            self.assertEqual(result[1], os.path.abspath(src))
            self.assertEqual(result[2], os.path.abspath(out_dir))


class TestValidateCommandArgs(unittest.TestCase):
    """Tests for _validate_command_args security validation."""

    def test_ampersand_in_arg_is_rejected(self) -> None:
        """Should return False when argument contains & character."""
        cmd = ["soffice", "--headless", "file&name.odt"]
        self.assertFalse(c._validate_command_args(cmd))

    def test_pipe_in_arg_is_rejected(self) -> None:
        """Should return False when argument contains | character."""
        cmd = ["soffice", "file|name.odt"]
        self.assertFalse(c._validate_command_args(cmd))

    def test_semicolon_in_arg_is_rejected(self) -> None:
        """Should return False when argument contains ; character."""
        cmd = ["soffice", "file;name.odt"]
        self.assertFalse(c._validate_command_args(cmd))

    def test_safe_arguments_are_accepted(self) -> None:
        """Should return True for valid safe arguments."""
        cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", "/tmp", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))

    def test_outdir_value_is_skipped(self) -> None:
        """Should skip the value after --outdir flag."""
        cmd = ["soffice", "--outdir", "/tmp/safe output", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))

    def test_convert_to_value_is_skipped(self) -> None:
        """Should skip the value after --convert-to flag."""
        cmd = ["soffice", "--convert-to", "pdf", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))

    def test_env_prefix_arg_is_skipped(self) -> None:
        """Should skip arguments starting with -env: prefix."""
        cmd = ["soffice", "-env:UserInstallation=file:///tmp/profile", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))

    def test_dash_arg_is_skipped(self) -> None:
        """Should skip arguments starting with - (flags)."""
        cmd = ["soffice", "--headless", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))


class TestConvertWithLibreoffice(unittest.TestCase):
    """Tests for _convert_with_libreoffice error handling."""

    def test_returns_false_when_source_does_not_exist(self) -> None:
        """Should return False when source file does not exist."""
        result = c._convert_with_libreoffice("nonexistent.odt", "output/test.pdf")
        self.assertFalse(result)

    def test_returns_false_on_timeout(self) -> None:
        """Should return False when LibreOffice conversion times out."""
        src = os.path.join(
            c.convert_vars.BASE_PATH, "resources", "templates", "owasp_cornucopia_webapp_ver_guide_bridge_en.odt"
        )
        out_dir = os.path.join(c.convert_vars.BASE_PATH, "output")
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "test_timeout.pdf")
        if os.path.exists(src):
            with mock.patch("subprocess.run", side_effect=subprocess.TimeoutExpired("soffice", 300)):
                result = c._convert_with_libreoffice(src, out)
                self.assertFalse(result)

    def test_returns_false_on_subprocess_exception(self) -> None:
        """Should return False when subprocess raises an exception."""
        src = os.path.join(
            c.convert_vars.BASE_PATH, "resources", "templates", "owasp_cornucopia_webapp_ver_guide_bridge_en.odt"
        )
        out_dir = os.path.join(c.convert_vars.BASE_PATH, "output")
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "test_exc.pdf")
        if os.path.exists(src):
            with mock.patch("subprocess.run", side_effect=Exception("LibreOffice not found")):
                result = c._convert_with_libreoffice(src, out)
                self.assertFalse(result)


class TestReplaceElementText(unittest.TestCase):
    """Tests for _replace_element_text XML text replacement."""

    def test_replaces_tag_in_element_text(self) -> None:
        """Should replace template tag in element text and return True."""
        el = ET.fromstring("<p>${Common_T01000}</p>")
        el.text = "${Common_T01000}"
        result = c._replace_element_text(el, [("${Common_T01000}", "Authentication")], False)
        self.assertTrue(result)
        self.assertEqual(el.text, "Authentication")

    def test_no_replacement_when_tag_not_present(self) -> None:
        """Should return False when no matching tag found in element."""
        el = ET.fromstring("<p>Static text</p>")
        el.text = "Static text"
        result = c._replace_element_text(el, [("${Common_T01000}", "Authentication")], False)
        self.assertFalse(result)
        self.assertEqual(el.text, "Static text")

    def test_replaces_tag_in_child_tail(self) -> None:
        """Should replace template tag stored in child element tail text."""
        el = ET.fromstring("<p><span/>${Common_T01000}</p>")
        child = list(el)[0]
        child.tail = "${Common_T01000}"
        result = c._replace_element_text(el, [("${Common_T01000}", "Authentication")], False)
        self.assertTrue(result)
        self.assertEqual(child.tail, "Authentication")

    def test_preserves_already_modified_true(self) -> None:
        """Should preserve True value of modified flag even when no replacement occurs."""
        el = ET.fromstring("<p>Static text</p>")
        el.text = "Static text"
        result = c._replace_element_text(el, [("${Common_T01000}", "Authentication")], True)
        self.assertTrue(result)


class TestCleanupTempFile(unittest.TestCase):
    """Tests for _cleanup_temp_file behavior in debug and normal modes."""

    def test_removes_file_when_not_in_debug_mode(self) -> None:
        """Should delete file when debug mode is off."""
        c.convert_vars.args = argparse.Namespace(debug=False)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp = f.name
        c._cleanup_temp_file(tmp)
        self.assertFalse(os.path.exists(tmp))

    def test_keeps_file_when_in_debug_mode(self) -> None:
        """Should keep file when debug mode is on."""
        c.convert_vars.args = argparse.Namespace(debug=True)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp = f.name
        try:
            c._cleanup_temp_file(tmp)
            self.assertTrue(os.path.exists(tmp))
        finally:
            os.unlink(tmp)

    def test_handles_missing_file_gracefully(self) -> None:
        """Should not raise exception when file does not exist."""
        c.convert_vars.args = argparse.Namespace(debug=False)
        c._cleanup_temp_file("this_file_does_not_exist.odt")


class TestIsValidStringArgument(unittest.TestCase):
    """Tests for is_valid_string_argument validation."""

    def test_raises_on_argument_over_255_chars(self) -> None:
        """Should raise ArgumentError when argument exceeds 255 characters."""
        long_arg = "a" * 256
        with self.assertRaises(argparse.ArgumentError):
            c.is_valid_string_argument(long_arg)

    def test_raises_on_invalid_characters(self) -> None:
        """Should raise ArgumentError when argument contains invalid characters."""
        with self.assertRaises(argparse.ArgumentError):
            c.is_valid_string_argument("invalid!@#$%^*()")


class TestIsValidArgumentList(unittest.TestCase):
    """Tests for is_valid_argument_list validation."""

    def test_returns_list_unchanged_when_valid(self) -> None:
        """Should return valid list unchanged."""
        result = c.is_valid_argument_list(["en", "fr", "de"])
        self.assertEqual(result, ["en", "fr", "de"])

    def test_returns_non_list_unchanged(self) -> None:
        """Should return non-list argument unchanged without validation."""
        result = c.is_valid_argument_list("en")
        self.assertEqual(result, "en")


if __name__ == "__main__":
    unittest.main()
