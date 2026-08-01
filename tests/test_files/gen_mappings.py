import argparse
import yaml
import qrcode  # type: ignore
import qrcode.image.svg  # type: ignore
from typing import Any, Dict
from security import safe_requests  # type: ignore

opencre_base_url = "https://opencre.org"
opencre_rest_url = "https://opencre.org/rest/v1"
CORNUCOPIA_VERSION = "1.20"
STANDARDS_TO_ADD = [
    "ASVS",
    "CAPEC",
    "SCP",
]


def make_cre_link(cre_id: str, frontend: bool = False) -> str:
    if frontend:
        return f"{opencre_base_url}/cre/{cre_id}"
    else:
        return f"{opencre_rest_url}/id/{cre_id}"


def produce_webapp_mappings(source_file: Dict[Any, Any], standards_to_add: list[str]) -> Dict[Any, Any]:
    base = {
        "meta": {"edition": "webapp", "component": "mappings", "language": "ALL", "version": CORNUCOPIA_VERSION},
    }
    for indx, suit in enumerate(source_file.copy()["suits"]):
        for card_indx, card in enumerate(suit["cards"]):
            cre = card["cre"][0]
            response = safe_requests.get(make_cre_link(cre), timeout=60)
            if response.status_code == 200:
                cre_object = response.json().get("data")
                for standard in standards_to_add:
                    for link in cre_object.get("links"):
                        if link.get("document").get("name") == standard:
                            source_file["suits"][indx]["cards"][card_indx][standard] = link.get("document").get(
                                "sectionID"
                            )
            else:
                print(f"could not find CRE {cre}, status code {response.status_code}")

    base["suits"] = source_file["suits"]
    return base


def generate_qr_images(existing_mappings: Dict[Any, Any], directory_path: str) -> None:
    for suit in existing_mappings["suits"]:
        for card in suit["cards"]:
            cre = card["cre"][0]
            link = make_cre_link(cre, frontend=True)
            print(f"making qr code for {cre}")
            img = qrcode.make(link, image_factory=qrcode.image.svg.SvgImage)
            with open(f"{directory_path}/{cre}", "wb") as f:
                img.save(f)


def main() -> None:
    global opencre_base_url, opencre_rest_url
    parser = argparse.ArgumentParser(description="generate mappings")
    parser.add_argument("-c", "--cres", help="Where to find the file mapping cornucopia to CREs", required=True)
    parser.add_argument("-t", "--target", help="Path where to store the result", required=True)
    parser.add_argument(
        "-s", "--staging", action="store_true", help="If provided will use staging.opencre.org instead of opencre.org"
    )
    parser.add_argument(
        "-q", "--qr_images", help="If provided will populate the target dir with qr image pointing to every cre"
    )
    args = vars(parser.parse_args())
    if args["staging"]:
        print("Using staging.opencre.org")
        opencre_base_url = "https://staging.opencre.org"
        opencre_rest_url = "https://staging.opencre.org/rest/v1"
    with open(args["cres"]) as f:
        mappings = yaml.safe_load(f)
        if args["target"]:
            webapp = produce_webapp_mappings(mappings, STANDARDS_TO_ADD)
            with open(args["target"], "w") as ef:
                yaml.safe_dump(webapp, ef)
        if args["qr_images"]:
            generate_qr_images(mappings, args["qr_images"])


if __name__ == "__main__":
    main()
