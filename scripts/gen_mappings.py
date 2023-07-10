import argparse
import yaml
import requests
from typing import Any, Dict

opencre_rest_url = "https://opencre.org/rest/v1"
CORNUCOPIA_VERSION = "1.20"
STANDARDS_TO_ADD = [
    "ASVS",
    "CAPEC",
    "OWASP Cheat Sheets",
    "OWASP Proactive Controls",
]


def make_mapping_link(mapping_id: str, mapping_type: str) -> str:
    if mapping_type == "cre":
        return f"{opencre_rest_url}/id/{mapping_id}"
    else:
        return f"{opencre_rest_url}/standard/{mapping_type}?sectionID={mapping_id}"


def produce_ecommerce_mappings(
    source_file: Dict[Any, Any], standards_to_add: list[str], mapping_type: str
) -> Dict[Any, Any]:
    base = {
        "meta": {"edition": "ecommerce", "component": "mappings", "language": "ALL", "version": CORNUCOPIA_VERSION},
    }
    for indx, suit in enumerate(source_file.copy()["suits"]):
        for card_indx, card in enumerate(suit["cards"]):
            for mapping_id in card[mapping_type]:
                response = requests.get(make_mapping_link(mapping_id, mapping_type))
                if response.status_code == 200:
                    map_object = response.json().get("data")
                    for standard in standards_to_add:
                        for link in map_object.get("links"):
                            if link.get("document").get("name") == standard:
                                source_file["suits"][indx]["cards"][card_indx][standard] = link.get("document").get(
                                    "sectionID"
                                )
                else:
                    print(f"could not find {mapping_type} {mapping_id}, status code {response.status_code}")

    base["suits"] = source_file["suits"]
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
    basefile = ""
    mapping_base = ""
    if args["cre"]:
        basefile = args["cre"]
        mapping_base = "cre"
    elif args["capec"]:
        basefile = args["capec"]
        mapping_base = "capec"
    with open(basefile) as f:
        mappings = yaml.safe_load(f)
        if args["target"]:
            ecommerce = produce_ecommerce_mappings(mappings, STANDARDS_TO_ADD, mapping_base)
            with open(args["target"], "w") as ef:
                yaml.safe_dump(ecommerce, ef)


if __name__ == "__main__":
    main()
