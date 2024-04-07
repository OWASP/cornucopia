import unittest
import argparse
import os
import platform
import docx  # type: ignore
import logging
import glob
import shutil
import typing
from typing import List, Dict, Any, Tuple
from unittest.mock import patch

import sys
import atheris

import scripts.convert as c
c.convert_vars = c.ConvertVars()

def TestOneInput(data):
  fdp = atheris.FuzzedDataProvider(data)
  input_key = fdp.ConsumeUnicodeNoSurrogates(1024)
  want_tags = ["VE", "AT", "SM", "AZ", "CR", "CO", "WC"]
  want_key = "cards"
  try:
    got_tags, got_key = c.get_suit_tags_and_key(input_key)
    #the_soup = BeautifulSoup(html_str, 'html.parser')
  except:
    # We do not want to deal with any errors right now
    return
  try:
    assert got_key == want_key
  except:
    pass

def main():
  atheris.instrument_all()
  atheris.Setup(sys.argv, TestOneInput)
  atheris.Fuzz()


if __name__ == "__main__":
  main()