import argparse
import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import atheris

import capec_map_enricher as enricher

enricher.enricher_vars = enricher.EnricherVars()


def _build_fuzzed_json(fdp):
    """Build a fuzzed CAPEC JSON structure from fuzz data."""
    capec_id = fdp.ConsumeUnicodeNoSurrogates(64)
    capec_name = fdp.ConsumeUnicodeNoSurrogates(64)
    cat_id = fdp.ConsumeUnicodeNoSurrogates(64)
    cat_name = fdp.ConsumeUnicodeNoSurrogates(64)
    return {
        "Attack_Pattern_Catalog": {
            "Attack_Patterns": {
                "Attack_Pattern": [
                    {"_ID": capec_id, "_Name": capec_name},
                ]
            },
            "Categories": {
                "Category": [
                    {"_ID": cat_id, "_Name": cat_name},
                ]
            },
        }
    }


def _build_fuzzed_yaml(fdp):
    """Build a fuzzed CAPEC-to-ASVS mapping dict from fuzz data."""
    capec_key = fdp.ConsumeUnicodeNoSurrogates(64)
    asvs_ref = fdp.ConsumeUnicodeNoSurrogates(64)
    return {
        "meta": {"version": "1.0"},
        capec_key: {"owasp_asvs": [asvs_ref]},
    }


def _run_enricher_main(test, argp, args):
    """Patch argparse and sys.argv, then run enricher.main(); swallow expected failures."""
    try:
        with patch.object(argparse, "ArgumentParser") as mock_parser:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.DEBUG):
                with patch("sys.argv", args):
                    enricher.main()
    except SystemExit:
        pass
    except Exception as exc:
        if "no logs of level" not in str(exc):
            raise


def test_main(data):
    """Atheris fuzz entry point for capec_map_enricher."""
    test = unittest.TestCase()
    test.maxDiff = None
    fdp = atheris.FuzzedDataProvider(data)

    fuzzed_edition = fdp.ConsumeUnicodeNoSurrogates(128)
    fuzzed_version = fdp.ConsumeUnicodeNoSurrogates(128)
    fuzzed_input = fdp.ConsumeUnicodeNoSurrogates(256)
    fuzzed_capec = fdp.ConsumeUnicodeNoSurrogates(256)

    base_path = Path(__file__).parent

    # --- Scenario 1: fuzzed edition and version ---
    args = ["-e", fuzzed_edition, "-v", fuzzed_version]
    argp = {
        "debug": True,
        "edition": fuzzed_edition,
        "version": fuzzed_version,
        "input_path": None,
        "source_dir": str(base_path),
        "output_path": None,
        "capec_json": str(base_path / "3000.json"),
    }
    _run_enricher_main(test, argp, args)

    # --- Scenario 2: fuzzed input_path ---
    args = ["-i", fuzzed_input]
    argp = {
        "debug": True,
        "edition": "webapp",
        "version": "latest",
        "input_path": fuzzed_input,
        "source_dir": str(base_path),
        "output_path": None,
        "capec_json": str(base_path / "3000.json"),
    }
    _run_enricher_main(test, argp, args)

    # --- Scenario 3: fuzzed capec_json path ---
    args = ["-c", fuzzed_capec]
    argp = {
        "debug": True,
        "edition": "webapp",
        "version": "latest",
        "input_path": None,
        "source_dir": str(base_path),
        "output_path": None,
        "capec_json": fuzzed_capec,
    }
    _run_enricher_main(test, argp, args)

    # --- Scenario 4: fuzz extract_capec_names directly ---
    fuzzed_json = _build_fuzzed_json(fdp)
    enricher.extract_capec_names(fuzzed_json)
    enricher.extract_capec_names({})
    enricher.extract_capec_names({"Attack_Pattern_Catalog": {}})

    # --- Scenario 5: fuzz enrich_capec_mappings directly ---
    fuzzed_yaml = _build_fuzzed_yaml(fdp)
    capec_names = enricher.extract_capec_names(fuzzed_json)
    enricher.enrich_capec_mappings(fuzzed_yaml, capec_names)
    enricher.enrich_capec_mappings({}, {})

    test.assertTrue(True)


def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, test_main)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
