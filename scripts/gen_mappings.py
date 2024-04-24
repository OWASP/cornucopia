import argparse
import yaml
import json
import qrcode  # type: ignore
import qrcode.image.svg  # type: ignore
from typing import Any, Dict

base_url = "https://github.com/OWASP/cornucopia/wiki/"


def produce_ecommerce_mappings(source_file: Dict[Any, Any], language_mapping: Dict[Any, Any]) -> Dict[Any, Any]:
    base = {
        "meta": {
            "edition": "ecommerce",
            "component": "mappings",
            "language": language_mapping["meta"]["language"],
            "version": language_mapping["meta"]["version"],
        },
        "standards": [],
    }
    for indx, suit in enumerate(source_file.copy()["suits"]):
        cards = language_mapping["suits"][indx]["cards"]
        for index, card in enumerate(suit["cards"]):
            standard = {
                "doctype": "Tool",
                "name": suit["name"],
                "section": cards[index]["desc"],
                "sectionID": suit["code"] + card["value"],
                "hyperlink": base_url + suit["code"] + card["value"],
                "links": [],
                "tags": [],
                "tooltype": "Defensive",
            }
            for cre in card["cre"]:
                standard["links"].append({"document": {"doctype": "CRE", "id": cre}})
            base["standards"].append(standard)  # type: ignore
    return base


def generate_qr_images(existing_mappings: Dict[Any, Any], directory_path: str) -> None:
    for suit in existing_mappings["suits"]:
        for card in suit["cards"]:
            link = base_url + suit["code"] + card["value"]
            img = qrcode.make(link, image_factory=qrcode.image.svg.SvgImage)
            base_name = suit["code"] + card["value"]
            with open(f"{directory_path}/{base_name}.svg", "wb") as f:
                img.save(f)


def main() -> None:
    global opencre_base_url, opencre_rest_url
    parser = argparse.ArgumentParser(description="generate mappings")
    parser.add_argument("-c", "--cres", help="Where to find the file mapping cornucopia to CREs", required=True)
    parser.add_argument(
        "-l",
        "--lang",
        help="Where to find the language file mapping CREs to the Cornucopia card scenarios",
        required=True,
    )
    parser.add_argument("-t", "--target", help="Path where to store the result", required=True)
    parser.add_argument(
        "-q", "--qr_images", help="If provided will populate the target dir with qr image pointing to every cre"
    )
    args = vars(parser.parse_args())
    with open(args["lang"]) as f:
        language_mapping = yaml.safe_load(f)
    with open(args["cres"]) as f:
        mappings = yaml.safe_load(f)
        if args["target"]:
            ecommerce = produce_ecommerce_mappings(mappings, language_mapping)
            with open(args["target"], "w") as ef:
                ef.write(json.dumps(ecommerce, indent=4))
        if args["qr_images"]:
            generate_qr_images(mappings, args["qr_images"])


if __name__ == "__main__":
    main()
