import unittest
import unittest.mock as mock
import os
import sys
import tempfile
import subprocess
import argparse

import scripts.convert as c

c.convert_vars = c.ConvertVars()
c.convert_vars.BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(c.__file__)))[0]


class TestValidateFilePaths(unittest.TestCase):
    def test_source_file_not_exist(self):
        result = c._validate_file_paths("nonexistent_file.odt", "output/test.pdf")
        self.assertFalse(result[0])
        self.assertIn("does not exist", result[1])

    def test_output_dir_not_exist(self):
        with tempfile.NamedTemporaryFile(suffix=".odt", delete=False) as f:
            tmp = f.name
        try:
            result = c._validate_file_paths(tmp, "/nonexistent_dir/test.pdf")
            self.assertFalse(result[0])
        finally:
            os.unlink(tmp)

    def test_source_outside_base(self):
        with tempfile.NamedTemporaryFile(suffix=".odt", delete=False, dir=tempfile.gettempdir()) as f:
            tmp = f.name
        try:
            result = c._validate_file_paths(tmp, os.path.join(c.convert_vars.BASE_PATH, "output", "test.pdf"))
            self.assertFalse(result[0])
        finally:
            os.unlink(tmp)

    def test_valid_paths(self):
        src = os.path.join(c.convert_vars.BASE_PATH, "resources", "templates",
                          "owasp_cornucopia_webapp_ver_guide_bridge_en.odt")
        out = os.path.join(c.convert_vars.BASE_PATH, "output", "test.pdf")
        if os.path.exists(src):
            result = c._validate_file_paths(src, out)
            self.assertTrue(result[0])


class TestValidateCommandArgs(unittest.TestCase):
    def test_dangerous_ampersand(self):
        cmd = ["soffice", "--headless", "file&name.odt"]
        self.assertFalse(c._validate_command_args(cmd))

    def test_dangerous_pipe(self):
        cmd = ["soffice", "file|name.odt"]
        self.assertFalse(c._validate_command_args(cmd))

    def test_dangerous_semicolon(self):
        cmd = ["soffice", "file;name.odt"]
        self.assertFalse(c._validate_command_args(cmd))

    def test_safe_args(self):
        cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", "/tmp", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))

    def test_skip_outdir_arg(self):
        cmd = ["soffice", "--outdir", "/tmp/safe", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))

    def test_skip_convert_to_arg(self):
        cmd = ["soffice", "--convert-to", "pdf", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))

    def test_env_prefix_skipped(self):
        cmd = ["soffice", "-env:UserInstallation=file:///tmp", "file.odt"]
        self.assertTrue(c._validate_command_args(cmd))


class TestConvertWithLibreoffice(unittest.TestCase):
    def test_invalid_source(self):
        result = c._convert_with_libreoffice("nonexistent.odt", "output/test.pdf")
        self.assertFalse(result)

    def test_timeout(self):
        with tempfile.NamedTemporaryFile(suffix=".odt",
                dir=c.convert_vars.BASE_PATH, delete=False) as f:
            tmp = f.name
        out = os.path.join(c.convert_vars.BASE_PATH, "output", "test.pdf")
        try:
            with mock.patch("subprocess.run", side_effect=subprocess.TimeoutExpired("soffice", 300)):
                result = c._convert_with_libreoffice(tmp, out)
                self.assertFalse(result)
        finally:
            os.unlink(tmp)

    def test_exception(self):
        with tempfile.NamedTemporaryFile(suffix=".odt",
                dir=c.convert_vars.BASE_PATH, delete=False) as f:
            tmp = f.name
        out = os.path.join(c.convert_vars.BASE_PATH, "output", "test.pdf")
        try:
            with mock.patch("subprocess.run", side_effect=Exception("conversion failed")):
                result = c._convert_with_libreoffice(tmp, out)
                self.assertFalse(result)
        finally:
            os.unlink(tmp)


class TestReplaceElementText(unittest.TestCase):
    def test_replace_text(self):
        import xml.etree.ElementTree as ET
        el = ET.fromstring("<p>Hello</p>")
        el.text = "${name}"
        result = c._replace_element_text(el, [("${name}", "World")], False)
        self.assertTrue(result)
        self.assertEqual(el.text, "World")

    def test_no_change(self):
        import xml.etree.ElementTree as ET
        el = ET.fromstring("<p>Hello</p>")
        el.text = "Hello"
        result = c._replace_element_text(el, [("${name}", "World")], False)
        self.assertFalse(result)

    def test_child_tail(self):
        import xml.etree.ElementTree as ET
        el = ET.fromstring("<p><b/>tail</p>")
        child = list(el)[0]
        child.tail = "${name}"
        result = c._replace_element_text(el, [("${name}", "World")], False)
        self.assertTrue(result)
        self.assertEqual(child.tail, "World")

    def test_modified_already_true(self):
        import xml.etree.ElementTree as ET
        el = ET.fromstring("<p>Hello</p>")
        el.text = "Hello"
        result = c._replace_element_text(el, [("${name}", "World")], True)
        self.assertTrue(result)


class TestConvertWithDocx2pdf(unittest.TestCase):
    def test_non_docx_returns_false(self):
        result = c._convert_with_docx2pdf("file.odt", "output/test.pdf")
        self.assertFalse(result)

    def test_docx_exception(self):
        c.convert_vars.can_convert_to_pdf = True
        with mock.patch.dict("sys.modules", {"docx2pdf": mock.MagicMock(
                convert=mock.MagicMock(side_effect=Exception("fail")))}):
            result = c._convert_with_docx2pdf("file.docx", "output/test.pdf")
            self.assertFalse(result)


class TestCleanupTempFile(unittest.TestCase):
    def test_cleanup_no_debug(self):
        c.convert_vars.args = argparse.Namespace(debug=False)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp = f.name
        c._cleanup_temp_file(tmp)
        self.assertFalse(os.path.exists(tmp))

    def test_cleanup_debug_mode(self):
        c.convert_vars.args = argparse.Namespace(debug=True)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp = f.name
        try:
            c._cleanup_temp_file(tmp)
            self.assertTrue(os.path.exists(tmp))
        finally:
            os.unlink(tmp)

    def test_cleanup_missing_file(self):
        c.convert_vars.args = argparse.Namespace(debug=False)
        c._cleanup_temp_file("nonexistent_file.odt")


class TestIsValidArgumentList(unittest.TestCase):
    def test_valid_list(self):
        result = c.is_valid_argument_list(["en", "fr", "de"])
        self.assertEqual(result, ["en", "fr", "de"])

    def test_not_a_list(self):
        result = c.is_valid_argument_list("en")
        self.assertEqual(result, "en")


if __name__ == "__main__":
    unittest.main()
