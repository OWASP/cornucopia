import sys
import os
import json
import tempfile
from pathlib import Path

import atheris

atheris.instrument_all()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

def TestOneInput(data):
    import scripts.convert_capec

    fdp = atheris.FuzzedDataProvider(data)
    asvs_version = fdp.ConsumeUnicodeNoSurrogates(50)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        input_json  = tmp / "capec.json"
        asvs_json   = tmp / "asvs.json"
        capec_map   = tmp / "capec_map.yaml"
        output_dir  = tmp / "out"

        output_dir.mkdir(exist_ok=True)

        input_json.write_text('{"dummy": true}', encoding="utf-8")
        asvs_json.write_text('{"dummy": true}', encoding="utf-8")
        capec_map.write_text("dummy: true", encoding="utf-8")

        sys.argv = [
            "convert_capec.py",
            "--output-path",     str(output_dir),
            "--input-path",      str(input_json),
            "--capec-to-asvs",   str(capec_map),
            "--asvs-mapping",    str(asvs_json),
            "--asvs-version",    asvs_version,
        ]

        try:
            scripts.convert_capec.main()
        except SystemExit as e:
            if e.code not in (0, None):
                atheris.write_test_error(f"Exited with code: {e.code}")
        except Exception as exc:
            atheris.write_test_error(f"{type(exc).__name__}: {exc}")


def main():
    atheris.Setup(
        sys.argv,
        TestOneInput,
        enable_python_coverage=True,
    )
    atheris.Fuzz()


if __name__ == "__main__":
    main()