import argparse
import yaml
import requests
from typing import Any, Dict

opencre_rest_url = "https://opencre.org/rest/v1"
CORNUCOPIA_VERSION = "1.20"
STANDARDS_FROM = ["CRE"]
STANDARDS_TO_ADD = [
    "ASVS",
    "CAPEC",
    "OWASP Cheat Sheets",
    "OWASP Proactive Controls",
]


def make_mapping_link(mapping_id: str, mapping_type: str) -> str:
    url = (
        f"{opencre_rest_url}/id/{mapping_id}"
        if mapping_type == "cre"
        else f"{opencre_rest_url}/standard/{mapping_type}?sectionID={mapping_id}"
    )
    return url


def produce_ecommerce_mappings(
    src_file: Dict[Any, Any], standards_to_add: list[str], mapping_type: str
) -> Dict[Any, Any]:
    base = {"meta": src_file.copy()["meta"]}
    for indx, suit in enumerate(src_file.copy()["suits"]):
        for card_indx, card in enumerate(suit["cards"]):
            for mapping_id in card[mapping_type]:
                response = requests.get(make_mapping_link(mapping_id, mapping_type))
                if response.status_code == 200:
                    if mapping_type == "capec":
                        map_type, map_name = "standards", "doctype"
                    else:
                        map_type, map_name = "data", "name"
                    map_object = response.json().get(map_type)
                    for std in standards_to_add:
                        map_id = "id" if std == "CRE" else "section" if std.startswith("OWASP ") else "sectionID"
                        try:
                            for link in map_object.get("links"):
                                if link.get("document").get(map_name) == std:
                                    src_file["suits"][indx]["cards"][card_indx][std] = link.get("document").get(map_id)
                        except AttributeError:
                            print(f"no links from {mapping_type} {mapping_id}")
                            continue
                else:
                    print(f"could not find {mapping_type} {mapping_id}, status code {response.status_code}")

    base["suits"] = src_file["suits"]
    return base


def main() -> None:
    global opencre_rest_url
    parser = argparse.ArgumentParser(description="generate mappings")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--cre", help="Where to find the file mapping cornucopia to CREs")
    group.add_argument("-k", "--capec", help="Where to find the file mapping cornucopia to CAPEC")
    parser.add_argument("-t", "--target", help="Path where to store the result", required=True)
    parser.add_argument(
        "-s", "--staging", action="store_true", help="If provided will use staging.opencre.org instead of opencre.org"
    )
    args = vars(parser.parse_args())
    basefile = mapping_base = standards_adding = ""
    if args["cre"]:
        basefile = args["cre"]
        mapping_base = "cre"
        standards_adding = STANDARDS_TO_ADD
    elif args["capec"]:
        basefile = args["capec"]
        mapping_base = "capec"
        standards_adding = STANDARDS_FROM
    with open(basefile) as f:
        mappings = yaml.safe_load(f)
        if args["target"]:
            ecommerce = produce_ecommerce_mappings(mappings, standards_adding, mapping_base)
            with open(args["target"], "w") as ef:
                yaml.safe_dump(ecommerce, ef, default_flow_style=None)


if __name__ == "__main__":
    main()
