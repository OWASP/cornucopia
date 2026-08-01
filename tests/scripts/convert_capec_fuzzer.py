import sys
import logging
from pathlib import Path

import atheris

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def TestOneInput(data):
    from scripts import convert_capec as target

    fdp = atheris.FuzzedDataProvider(data)
    logging.getLogger().setLevel(logging.CRITICAL)

    asvs_version = fdp.ConsumeUnicodeNoSurrogates(50)

    sys.argv = [
        "convert_capec.py",
        "--output-path",
        "out",
        "--input-path",
        "in.json",
        "--capec-to-asvs",
        "map.yaml",
        "--asvs-mapping",
        "asvs.json",
        "--asvs-version",
        asvs_version,
    ]

    try:
        target.main()
    except SystemExit:
        pass
    except Exception:
        pass


def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
