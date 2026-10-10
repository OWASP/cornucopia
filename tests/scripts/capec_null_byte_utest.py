import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
import capec_map_enricher as enricher


class TestNullByteValidation(unittest.TestCase):
    """Test null byte validation in parse_arguments"""

    def test_null_byte_in_capec_json_path(self):
        with self.assertRaises(SystemExit) as ctx:
            enricher.parse_arguments(["-c", "path/to\x00file.json"])
        self.assertEqual(ctx.exception.code, 2)

    def test_null_byte_in_input_path(self):
        with self.assertRaises(SystemExit) as ctx:
            enricher.parse_arguments(["-i", "path/to\x00file.yaml"])
        self.assertEqual(ctx.exception.code, 2)

    def test_null_byte_in_source_dir(self):
        with self.assertRaises(SystemExit) as ctx:
            enricher.parse_arguments(["-s", "path/to\x00dir"])
        self.assertEqual(ctx.exception.code, 2)

    def test_null_byte_in_output_path(self):
        with self.assertRaises(SystemExit) as ctx:
            enricher.parse_arguments(["-o", "path/to\x00output.yaml"])
        self.assertEqual(ctx.exception.code, 2)

    def test_null_byte_in_version(self):
        with self.assertRaises(SystemExit) as ctx:
            enricher.parse_arguments(["-v", "3.0\x00malicious"])
        self.assertEqual(ctx.exception.code, 2)

    def test_null_byte_in_edition(self):
        with self.assertRaises(SystemExit) as ctx:
            enricher.parse_arguments(["-e", "webapp\x00malicious"])
        self.assertEqual(ctx.exception.code, 2)

    def test_valid_paths_not_rejected(self):
        args = enricher.parse_arguments(["-v", "3.0", "-e", "mobileapp"])
        self.assertEqual(args.version, "3.0")
        self.assertEqual(args.edition, "mobileapp")


if __name__ == "__main__":
    unittest.main()
