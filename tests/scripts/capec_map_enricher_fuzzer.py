#!/usr/bin/env python3
import argparse
import logging
import sys
import atheris
import os
import unittest
from unittest.mock import patch

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

    capec_json  = fdp.ConsumeUnicodeNoSurrogates(128)
    input_path  = fdp.ConsumeUnicodeNoSurrogates(128)
    version     = fdp.ConsumeUnicodeNoSurrogates(32)
    edition     = fdp.ConsumeUnicodeNoSurrogates(32)
    source_dir  = fdp.ConsumeUnicodeNoSurrogates(128)
    output_path = fdp.ConsumeUnicodeNoSurrogates(128)

    fuzzed_json_data = {
        "Attack_Pattern_Catalog": {
            "Attack_Patterns": {
                "Attack_Pattern": [
                    {
                        "_ID": (
                            str(fdp.ConsumeIntInRange(1, 10000))
                            if fdp.ConsumeBool()
                            else fdp.ConsumeUnicodeNoSurrogates(10)
                        ),
                        "_Name": fdp.ConsumeUnicodeNoSurrogates(128),
                    }
                    for _ in range(fdp.ConsumeIntInRange(0, 5))
                ]
            },
            "Categories": {
                "Category": [
                    {
                        "_ID": (
                            str(fdp.ConsumeIntInRange(1, 10000))
                            if fdp.ConsumeBool()
                            else fdp.ConsumeUnicodeNoSurrogates(10)
                        ),
                        "_Name": fdp.ConsumeUnicodeNoSurrogates(128),
                    }
                    for _ in range(fdp.ConsumeIntInRange(0, 5))
                ]
            },
        }
    }

    fuzzed_yaml_data = {}
    for _ in range(fdp.ConsumeIntInRange(0, 5)):
        key = fdp.ConsumeIntInRange(1, 10000)
        fuzzed_yaml_data[key] = {
            "owasp_asvs": [
                fdp.ConsumeUnicodeNoSurrogates(16)
                for _ in range(fdp.ConsumeIntInRange(0, 3))
            ]
        }

    # --- Fuzz version argument ---
    argp = {
        "capec_json": capec_json,
        "input_path": None,
        "version": version,
        "edition": "webapp",
        "source_dir": source_dir,
        "output_path": None,
        "debug": True,
    }
    try:
        with patch.object(enricher, "load_json_file", return_value=fuzzed_json_data), \
             patch.object(enricher, "load_yaml_file", return_value=fuzzed_yaml_data), \
             patch.object(enricher, "save_yaml_file", return_value=True), \
             patch.object(enricher, "parse_arguments", return_value=argparse.Namespace(**argp)), \
             patch("sys.argv", ["capec_map_enricher.py"]):
            with test.assertLogs(logging.getLogger(), logging.DEBUG):
                enricher.main()
    except SystemExit:
        pass
    except Exception as e:
        if "no logs of level" not in str(e):
            raise

    # --- Fuzz edition argument ---
    argp = {
        "capec_json": capec_json,
        "input_path": None,
        "version": "latest",
        "edition": edition,
        "source_dir": source_dir,
        "output_path": None,
        "debug": True,
    }
    try:
        with patch.object(enricher, "load_json_file", return_value=fuzzed_json_data), \
             patch.object(enricher, "load_yaml_file", return_value=fuzzed_yaml_data), \
             patch.object(enricher, "save_yaml_file", return_value=True), \
             patch.object(enricher, "parse_arguments", return_value=argparse.Namespace(**argp)), \
             patch("sys.argv", ["capec_map_enricher.py"]):
            with test.assertLogs(logging.getLogger(), logging.DEBUG):
                enricher.main()
    except SystemExit:
        pass
    except Exception as e:
        if "no logs of level" not in str(e):
            raise

    # --- Fuzz input_path argument ---
    argp = {
        "capec_json": capec_json,
        "input_path": input_path,
        "version": "latest",
        "edition": "webapp",
        "source_dir": source_dir,
        "output_path": None,
        "debug": True,
    }
    try:
        with patch.object(enricher, "load_json_file", return_value=fuzzed_json_data), \
             patch.object(enricher, "load_yaml_file", return_value=fuzzed_yaml_data), \
             patch.object(enricher, "save_yaml_file", return_value=True), \
             patch.object(enricher, "parse_arguments", return_value=argparse.Namespace(**argp)), \
             patch("sys.argv", ["capec_map_enricher.py"]):
            with test.assertLogs(logging.getLogger(), logging.DEBUG):
                enricher.main()
    except SystemExit:
        pass
    except Exception as e:
        if "no logs of level" not in str(e):
            raise

    # --- Fuzz output_path argument ---
    argp = {
        "capec_json": capec_json,
        "input_path": input_path,
        "version": "latest",
        "edition": "webapp",
        "source_dir": source_dir,
        "output_path": output_path,
        "debug": True,
    }
    try:
        with patch.object(enricher, "load_json_file", return_value=fuzzed_json_data), \
             patch.object(enricher, "load_yaml_file", return_value=fuzzed_yaml_data), \
             patch.object(enricher, "save_yaml_file", return_value=True), \
             patch.object(enricher, "parse_arguments", return_value=argparse.Namespace(**argp)), \
             patch("sys.argv", ["capec_map_enricher.py"]):
            with test.assertLogs(logging.getLogger(), logging.DEBUG):
                enricher.main()
    except SystemExit:
        pass
    except Exception as e:
        if "no logs of level" not in str(e):
            raise

    # --- Fuzz capec_json path argument ---
    argp = {
        "capec_json": capec_json,
        "input_path": input_path,
        "version": "latest",
        "edition": "webapp",
        "source_dir": source_dir,
        "output_path": output_path,
        "debug": True,
    }
    try:
        with patch.object(enricher, "load_json_file", return_value=fuzzed_json_data), \
             patch.object(enricher, "load_yaml_file", return_value=fuzzed_yaml_data), \
             patch.object(enricher, "save_yaml_file", return_value=True), \
             patch.object(enricher, "parse_arguments", return_value=argparse.Namespace(**argp)), \
             patch("sys.argv", ["capec_map_enricher.py"]):
            with test.assertLogs(logging.getLogger(), logging.DEBUG):
                enricher.main()
    except SystemExit:
        pass
    except Exception as e:
        if "no logs of level" not in str(e):
            raise

    test.assertTrue(True)


def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, test_main)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
