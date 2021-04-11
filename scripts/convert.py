#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
import yaml
from typing import List, TextIO


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
        level=logging.INFO,
    )
    args = parse_arguments(sys.argv[1:])
    if args.output:
        for file in source_location:
            yaml.load()


def parse_arguments(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tool to convert.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--output",
        type=str,
        choices=["json", "pdf", "indd"],
        default=None,
        help="Output format to produce.",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    main()
