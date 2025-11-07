"""
Script: generate_webapp_capec.py

Creates a new YAML file that maps CAPEC numbers to their associated OWASP ASVS requirements.
Only includes CAPEC numbers that appear in 'capec' lists, and only includes ASVS requirements
from matching entries in 'capec_map'.

Behavior / contract
- Input: webapp-mappings-3.0.yaml (contains cards with capec lists and capec_map entries)
- Output: webapp-capec-3.0.yaml (contains only CAPEC to ASVS mapping)

Process:
1. First collects all CAPEC numbers found in 'capec' lists
2. For each of these numbers:
   - Searches through all 'capec_map' entries in the input file
   - If the number exists as a key in a capec_map
   - Adds that mapping's owasp_asvs strings to our output

Example input (webapp-mappings-3.0.yaml):
  capec: [54, 113]  # These numbers will be in output
  capec_map:
    54:  
      owasp_asvs: ["4.3.2"]  # Will be under "54"
    113:
      owasp_asvs: ["5.1.1"]  # Will be under "113"
    116:  # Won't be in output (not in capec list)
      owasp_asvs: ["7.1.1"]

Example output (webapp-capec-3.0.yaml):

CAPEC:
  <capec-number>:
    owasp_asvs:
      - <ASVS string>

Notes / assumptions
- The script tries to be forgiving: `capec_map` values may be dicts, lists of dicts, lists of numbers/strings.
- `owasp_asvs` is expected to be a list of strings; non-list values are ignored with a warning.

Usage:
  python scripts/generate_webapp_capec.py \
    --input source/webapp-mappings-3.0.yaml \
    --output source/webapp-capec-3.0.yaml

"""
from __future__ import annotations
import argparse
import sys
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

try:
    import yaml
except Exception as e:
    print("Missing dependency: PyYAML is required. Install with `pip install pyyaml`.")
    raise


def find_mapping_nodes_with_keys(obj: Any, keys: Iterable[str]):
    """Recursively walk `obj` (list/dict) and yield dict nodes that contain ALL keys in `keys`.

    Yields the dict node itself.
    """
    needed = set(keys)
    
    if isinstance(obj, dict):
        logging.info(f"Visiting dict node with keys: {list(obj.keys())}")
        if needed.issubset(obj.keys()):
            logging.info(f"Found mapping node with keys {keys}: {obj}")
            yield obj
        for v in obj.values():
            yield from find_mapping_nodes_with_keys(v, keys)
    elif isinstance(obj, list):
        for item in obj:
            yield from find_mapping_nodes_with_keys(item, keys)


def extract_capec_numbers(capec_map_value: Any) -> List[str]:
    """Return a list of CAPEC numbers (as strings) found in capec_map_value.

    Accepts several shapes:
    - dict mapping str->list or str->something
    - list of numbers/strings or list of dicts
    - a plain number/string
    """
    result: List[str] = []

    if capec_map_value is None:
        return result

    if isinstance(capec_map_value, dict):
        # Keys might be the capec numbers, or values may be lists of numbers
        for k, v in capec_map_value.items():
            # If key looks like a number, include it
            if isinstance(k, (str, int)) and str(k).strip() != "":
                result.append(str(k))
            # If value is a list of numbers/strings, include them
            if isinstance(v, (list, tuple)):
                for item in v:
                    if item is None:
                        continue
                    if isinstance(item, (str, int)):
                        s = str(item).strip()
                        if s:
                            result.append(s)
                    elif isinstance(item, dict):
                        # include dict keys too
                        for kk in item.keys():
                            result.append(str(kk))
            else:
                # non-list value might be a single number/string
                if isinstance(v, (str, int)) and str(v).strip() != "":
                    result.append(str(v))
    elif isinstance(capec_map_value, (list, tuple)):
        for item in capec_map_value:
            if isinstance(item, (str, int)):
                s = str(item).strip()
                if s:
                    result.append(s)
            elif isinstance(item, dict):
                # dict inside list: treat keys as numbers
                for kk in item.keys():
                    result.append(str(kk))
            elif isinstance(item, (list, tuple)):
                # nested list
                for nested in item:
                    if isinstance(nested, (str, int)):
                        result.append(str(nested))
    elif isinstance(capec_map_value, (str, int)):
        s = str(capec_map_value).strip()
        if s:
            result.append(s)

    # normalize and deduplicate while preserving insertion order
    seen: Set[str] = set()
    normalized: List[str] = []
    for r in result:
        if r not in seen:
            seen.add(r)
            normalized.append(r)
    return normalized


def extract_owasp_asvs_list(value: Any) -> List[str]:
    """Return a list of strings from owasp_asvs value; if not a list, return empty list.
    Non-string items are coerced to strings.
    """
    if not isinstance(value, (list, tuple)):
        return []
    out: List[str] = []
    for item in value:
        if item is None:
            continue
        out.append(str(item))
    # deduplicate while preserving order
    seen: Set[str] = set()
    res: List[str] = []
    for s in out:
        if s not in seen:
            seen.add(s)
            res.append(s)
    return res


def build_capec_mapping(data: Any) -> Dict[str, Set[str]]:
    """Walk the loaded YAML and build capec_num -> set(owasp_asvs strings).

    The algorithm:
    - For each node containing 'capec', look at its 'capec' list
    - For each number in that 'capec' list, look up that number in the node's capec_map
    - If found, add those specific owasp_asvs strings to our output mapping
    """
    mapping: Dict[str, Set[str]] = {}
    logging.info("Building CAPEC mapping from data")
    node_count = 0

    # First collect all CAPEC numbers from 'capec' lists
    for node in find_mapping_nodes_with_keys(data, ("capec",)):
        node_count += 1
        capec_list = node.get("capec", [])
        
        if not capec_list:
            logging.debug("Skipping node with empty capec list")
            continue
            
        # Convert capec list to set of strings for matching
        capec_nums = set(str(x).strip() for x in capec_list if x != "-")
        
        # Initialize mapping for each CAPEC number
        for num in capec_nums:
            if num not in mapping:
                mapping[num] = set()
                logging.debug(f"Added CAPEC number {num} to mapping")

    # Then find corresponding owasp_asvs strings from capec_map entries
    logging.info(f"Looking for ASVS requirements for {len(mapping)} CAPEC numbers")
    for num in mapping:
        logging.debug(f"Searching for CAPEC {num} in capec_map entries")
        for node in find_mapping_nodes_with_keys(data, ("capec_map",)):
            capec_val = node.get("capec_map", {})
            if not isinstance(capec_val, dict):
                logging.warning(f"Found invalid capec_map (not a dict): {capec_val}")
                continue

            if num in capec_val:
                logging.debug(f"Found CAPEC {num} in capec_map entry")
                mapping_entry = capec_val[num]
                if not isinstance(mapping_entry, dict):
                    logging.warning(f"Expected dict for capec_map.{num}, got {type(mapping_entry)}")
                    continue
                    
                asvs_list = mapping_entry.get("owasp_asvs", [])
                if not isinstance(asvs_list, (list, tuple)):
                    logging.warning(f"Expected list for capec_map.{num}.owasp_asvs, got {type(asvs_list)}")
                    continue
                
                # Add all ASVS strings for this CAPEC number
                valid_strings = [str(x) for x in asvs_list if x is not None and str(x).strip()]
                if valid_strings:
                    logging.debug(f"Adding {len(valid_strings)} ASVS strings to CAPEC {num}: {valid_strings}")
                    mapping[num].update(valid_strings)
                else:
                    logging.warning(f"No valid ASVS strings found for CAPEC {num}")
    
    return mapping
    
    return mapping


def format_output_structure(mapping: Dict[str, Set[str]]) -> Dict[str, Any]:
    """Return a YAML-serializable structure matching the requested output shape.

    Output shape:
    CAPEC:
      <num1>:
        owasp_asvs:
          - <string1>
          - <string2>
      <num2>:
        owasp_asvs:
          - <string3>
          ...
    """
    capec_out: Dict[str, Any] = {}
    # Sort CAPEC numbers numerically when possible
    for num in sorted(mapping, key=lambda x: (int(x) if x.isdigit() else x)):
        # Sort the ASVS strings for consistent output
        asvs_list = sorted(mapping[num]) if mapping[num] else []
        capec_out[str(num)] = {"owasp_asvs": asvs_list}
    return {"CAPEC": capec_out}

def set_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
    )
    if gen_capec_vars.args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


class GenCapecVars:
    args: argparse.Namespace


def parse_arguments(input_args: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate webapp-capec-3.0.yaml from webapp-mappings-3.0.yaml")
    p.add_argument("--input", "-i", default="source/webapp-mappings-3.0.yaml",
                   help="Input YAML file to scan (default: source/webapp-mappings-3.0.yaml)")
    p.add_argument("--output", "-o", default="source/webapp-capec-3.0.yaml",
                   help="Output YAML file to write (default: source/webapp-capec-3.0.yaml)")
    p.add_argument("--force", "-f", action="store_true", help="Overwrite existing output without asking")
    p.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Output additional information to debug script",
    )
    try:
        args = p.parse_args(input_args)
    except argparse.ArgumentError as exc:
        # sys.tracebacklimit = 0
        logging.error(exc.message)
        sys.exit()
    return args

def main(argv: List[str] | None = None) -> int:
    gen_capec_vars.args = parse_arguments(sys.argv[1:])
    set_logging()

    in_path = Path(gen_capec_vars.args.input)
    out_path = Path(gen_capec_vars.args.output)

    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        return 2

    if out_path.exists() and not gen_capec_vars.args.force:
        print(f"Output file {out_path} already exists. Use --force to overwrite.")
        return 3

    try:
        with in_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logging.error(f"Failed to parse YAML file {in_path}: {e}")
        return 1
    except Exception as e:
        logging.error(f"Failed to read file {in_path}: {e}")
        return 1

    if not isinstance(data, dict):
        logging.error(f"Expected YAML root to be a mapping/dict, got {type(data)}")
        return 1

    mapping = build_capec_mapping(data)

    out_struct = format_output_structure(mapping)

    # write output YAML
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(out_struct, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {out_path} with {len(mapping)} CAPEC entries.")
    return 0


if __name__ == "__main__":
    gen_capec_vars: GenCapecVars = GenCapecVars()
    raise SystemExit(main())
