#!/usr/bin/env python3
import argparse
import logging
import unittest
from unittest.mock import patch
import sys
import atheris
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts")))

try:
    import scripts.capec_map_enricher as enricher
except ImportError:
    import capec_map_enricher as enricher

enricher.enricher_vars = enricher.EnricherVars()
enricher.enricher_vars.args = argparse.Namespace(
    capec_json="",
    input_path=None,
    version="latest",
    edition="webapp",
    source_dir="",
    output_path=None,
    debug=False,
)


def test_main(data):
    test = unittest.TestCase()
    fdp = atheris.FuzzedDataProvider(data)
    capec_json = fdp.ConsumeUnicodeNoSurrogates(1024)
    input_path = fdp.ConsumeUnicodeNoSurrogates(1024)
    version = fdp.ConsumeUnicodeNoSurrogates(1024)
    edition = fdp.ConsumeUnicodeNoSurrogates(1024)
    source_dir = fdp.ConsumeUnicodeNoSurrogates(1024)
    output_path = fdp.ConsumeUnicodeNoSurrogates(1024)

    try:
        with patch.object(argparse, "ArgumentParser") as mock_parser:
            # --- Fuzz version argument ---
            args = ["-v", version, "-e", "webapp", "-s", source_dir]
            argp = {
                "debug": True,
                "capec_json": capec_json,
                "input_path": None,
                "version": version,
                "edition": "webapp",
                "source_dir": source_dir,
                "output_path": None,
            }
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.DEBUG) as l6:
                with patch("sys.argv", args):
                    enricher.main()

            # --- Fuzz edition argument ---
            args = ["-v", "latest", "-e", edition, "-s", source_dir]
            argp = {
                "debug": True,
                "capec_json": capec_json,
                "input_path": None,
                "version": "latest",
                "edition": edition,
                "source_dir": source_dir,
                "output_path": None,
            }
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.DEBUG) as l6:
                with patch("sys.argv", args):
                    enricher.main()

            # --- Fuzz input_path argument ---
            args = ["-v", "latest", "-e", "webapp", "-s", source_dir, "-i", input_path]
            argp = {
                "debug": True,
                "capec_json": capec_json,
                "input_path": input_path,
                "version": "latest",
                "edition": "webapp",
                "source_dir": source_dir,
                "output_path": None,
            }
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.DEBUG) as l6:
                with patch("sys.argv", args):
                    enricher.main()

            # --- Fuzz output_path argument ---
            args = ["-v", "latest", "-e", "webapp", "-s", source_dir, "-i", input_path, "-o", output_path]
            argp = {
                "debug": True,
                "capec_json": capec_json,
                "input_path": input_path,
                "version": "latest",
                "edition": "webapp",
                "source_dir": source_dir,
                "output_path": output_path,
            }
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.DEBUG) as l6:
                with patch("sys.argv", args):
                    enricher.main()

            # --- Fuzz capec_json argument ---
            args = ["-v", "latest", "-e", "webapp", "-s", source_dir, "-c", capec_json]
            argp = {
                "debug": True,
                "capec_json": capec_json,
                "input_path": None,
                "version": "latest",
                "edition": "webapp",
                "source_dir": source_dir,
                "output_path": None,
            }
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.DEBUG) as l6:
                with patch("sys.argv", args):
                    enricher.main()

    except Exception as e:
        print(e)
        print(f"{l6}")
        if "no logs of level" not in str(e):
            raise Exception("Enricher main died!")
    test.assertTrue(True)


def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, test_main)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
