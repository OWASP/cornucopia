import argparse
import yaml
import requests
from typing import Dict, List, Any
import time

opencre_rest_url = "https://opencre.org/rest/v1"
CORNUCOPIA_VERSION = "1.20"
STANDARDS_FROM = ["cre"]
STANDARDS_TO_ADD = {
    "ASVS": "owasp_asvs",
    "OWASP Cheat Sheets": "owasp_cheat_sheets",
    "OWASP Proactive Controls": "owasp_proactive_controls",
}


def make_mapping_link(mapping_id: str, mapping_type: str) -> str:
    url = (
        f"{opencre_rest_url}/id/{mapping_id}"
        if mapping_type == "cre"
        else f"{opencre_rest_url}/standard/{mapping_type}?sectionID={mapping_id}"
    )
    return url


def produce_ecommerce_mappings(
    src_file: Dict[str, Any], standards_to_add: Dict[str, Any], mapping_base: str, map_type: str, map_name: str
) -> Dict[str, Any]:
    base = {"meta": src_file["meta"]}
    suits = base["suits"] = src_file["suits"]

    for suit in suits:
        for card in suit["cards"]:
            mapping_ids = card.get(mapping_base, [])
            for mapping_id in mapping_ids:
                response = requests.get(make_mapping_link(mapping_id, mapping_base))
                if response.status_code != 200:
                    print(f"Could not find {mapping_base} {mapping_id}, status code {response.status_code}")
                    continue

                map_object = response.json().get(map_type)
                time.sleep(1)  # Important as Cloudflare throttled me

                if map_type == "standards":
                    map_object = map_object[0]

                for std_name in list(standards_to_add):
                    map_id = "id" if std_name == "cre" else "section" if std_name.startswith("OWASP ") else "sectionID"
                    links = map_object.get("links", [])
                    for link in links:
                        document = link.get("document", {})
                        if document.get(map_name, "").lower() == std_name.lower():
                            std_card = card.setdefault(std_name, [])
                            std_card.append(document.get(map_id))
                    std_card = list(dict.fromkeys(std_card))
    return base


def main() -> None:
    global opencre_rest_url
    parser = argparse.ArgumentParser(description="generate mappings")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--cre", help="Where to find the file mapping cornucopia to CREs")
    group.add_argument("-k", "--capec", help="Where to find the file mapping cornucopia to CAPEC")
    parser.add_argument("-t", "--target", help="Path where to store the result", required=True)
    args = vars(parser.parse_args())
    basefile = map_base = map_type = map_name = ""
    stds_to_add = []
    if args["cre"]:
        basefile = args["cre"]
        map_base = "cre"
        map_type = "data"
        map_name = "name"
        stds_to_add = STANDARDS_TO_ADD
    elif args["capec"]:
        basefile = args["capec"]
        map_base = "capec"
        map_type = "standards"
        map_name = "doctype"
        stds_to_add = STANDARDS_FROM
    with open(basefile) as f:
        mappings = yaml.safe_load(f)
        if args["target"]:
            ecommerce = produce_ecommerce_mappings(mappings, stds_to_add, map_base, map_type, map_name)
            with open(args["target"], "w") as ef:
                yaml.safe_dump(ecommerce, ef, default_flow_style=None)


if __name__ == "__main__":
    main()
