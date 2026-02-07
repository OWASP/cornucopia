import sys
import os
import json
import tempfile
import unittest
import argparse
import logging
from unittest.mock import patch
from pathlib import Path

logging.disable(logging.CRITICAL)

import atheris

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def TestOneInput(data):
    from scripts import convert_capec as c

    test = unittest.TestCase()
    fdp = atheris.FuzzedDataProvider(data)

    asvs_version = fdp.ConsumeUnicodeNoSurrogates(8)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_json = os.path.join(tmpdir, "capec.json")
        asvs_json = os.path.join(tmpdir, "asvs.json")
        capec_map = os.path.join(tmpdir, "capec_map.yaml")
        output_dir = os.path.join(tmpdir, "out")

        with open(input_json, "w", encoding="utf-8") as f:
            json.dump(
                {"Attack_Pattern_Catalog": {"Attack_Patterns": {"Attack_Pattern": []}}},
                f,
            )

        with open(asvs_json, "w", encoding="utf-8") as f:
            json.dump({"Requirements": []}, f)

        with open(capec_map, "w", encoding="utf-8") as f:
            f.write("1:\n  owasp_asvs: []\n")

        args = argparse.Namespace(
            output_path=output_dir,
            input_path=input_json,
            capec_to_asvs=capec_map,
            asvs_mapping=asvs_json,
            asvs_version=asvs_version,
            debug=False,
        )

        try:
            with patch.object(argparse.ArgumentParser, "parse_args", return_value=args):
                c.main()
        except SystemExit:
            pass
 
def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
