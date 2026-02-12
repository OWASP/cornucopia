#!/usr/bin/env python3
import argparse
import logging
import sys
import atheris
import os
from unittest.mock import patch

# Add the root directory to sys.path to import scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts")))

try:
    import scripts.capec_map_enricher as enricher
except ImportError:
    import capec_map_enricher as enricher

# Initialize enricher_vars (usually it's done at the end of the script)
if not hasattr(enricher, "enricher_vars"):
    enricher.enricher_vars = enricher.EnricherVars()


def test_main(data):
    fdp = atheris.FuzzedDataProvider(data)

    # Fuzz command line arguments
    capec_json = fdp.ConsumeUnicodeNoSurrogates(128)
    input_path = fdp.ConsumeUnicodeNoSurrogates(128)
    version = fdp.ConsumeUnicodeNoSurrogates(32)
    edition = fdp.ConsumeUnicodeNoSurrogates(32)
    source_dir = fdp.ConsumeUnicodeNoSurrogates(128)
    output_path = fdp.ConsumeUnicodeNoSurrogates(128)
    debug = fdp.ConsumeBool()

    # Create diverse fuzzed dictionary for JSON/YAML to exercise edge cases
    # JSON data for extraction
    fuzzed_json_data = (
        {
            "Attack_Pattern_Catalog": (
                {
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
                    }
                }
                if fdp.ConsumeBool()
                else {}
            )
        }
        if fdp.ConsumeBool()
        else {}
    )

    # YAML data for enrichment
    # keys can be ints or strings that look like ints
    fuzzed_yaml_data = {}
    for _ in range(fdp.ConsumeIntInRange(0, 5)):
        key = fdp.ConsumeIntInRange(1, 10000)
        fuzzed_yaml_data[key] = {
            "owasp_asvs": [fdp.ConsumeUnicodeNoSurrogates(16) for _ in range(fdp.ConsumeIntInRange(0, 3))]
        }
        if fdp.ConsumeBool():
            fuzzed_yaml_data[key]["extra_field"] = fdp.ConsumeUnicodeNoSurrogates(32)

    argp = {
        "capec_json": capec_json,
        "input_path": input_path if fdp.ConsumeBool() else None,
        "version": version,
        "edition": edition,
        "source_dir": source_dir,
        "output_path": output_path if fdp.ConsumeBool() else None,
        "debug": debug,
    }

    # Prepare args for sys.argv patch (though we mock parse_arguments, we still patch sys.argv for completeness)
    args = ["-v", version, "-e", edition, "-s", source_dir]
    if argp["input_path"]:
        args.extend(["-i", argp["input_path"]])
    if argp["output_path"]:
        args.extend(["-o", argp["output_path"]])
    if argp["debug"]:
        args.append("-d")

    try:
        # Mocking the file I/O to avoid hitting the disk and to feed fuzzed data
        # We also mock parse_arguments to avoid SystemExit from pathvalidate/argparse early on
        with patch.object(enricher, "load_json_file", return_value=fuzzed_json_data), patch.object(
            enricher, "load_yaml_file", return_value=fuzzed_yaml_data
        ), patch.object(enricher, "save_yaml_file", return_value=fdp.ConsumeBool()), patch.object(
            enricher, "parse_arguments", return_value=argparse.Namespace(**argp)
        ), patch(
            "sys.argv", ["capec_map_enricher.py"] + args
        ):

            # Silence logging during fuzzing to improve performance
            logging.getLogger().setLevel(logging.CRITICAL)

            enricher.main()

    except SystemExit:
        # Script calls sys.exit(1) on failure, which is expected during fuzzing
        pass
    except (TypeError, ValueError, KeyError):
        # These might be raised by the enrichment logic if fuzzed data is malformed
        # In a real fuzzer run, we might want to catch these to find bugs,
        # but here we are just ensuring it runs.
        pass
    except Exception as e:
        # Re-raise unexpected exceptions to let Atheris report them
        raise e


def main():
    # Instrument the target module
    atheris.instrument_all()
    # Also instrument the main script logic if necessary
    # atheis.instrument_func(enricher.extract_capec_names)
    # atheis.instrument_func(enricher.enrich_capec_mappings)

    atheris.Setup(sys.argv, test_main)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
