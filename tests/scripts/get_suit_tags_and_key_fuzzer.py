import unittest
from typing import List
import sys
import atheris

import convert as c

c.convert_vars = c.ConvertVars()


def TestOneInput(data):
    test = unittest.TestCase()
    fdp = atheris.FuzzedDataProvider(data)
    input_key = fdp.ConsumeUnicodeNoSurrogates(1024)
    want_tags: List[str] = []
    want_key: str = ""
    got_tags, got_key = c.get_suit_tags_and_key(input_key)
    assert got_key == want_key
    test.assertEqual(want_tags, got_tags)


def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
