import itertools
import yaml
from pprint import pprint
import requests
import re

mappings = list(yaml.safe_load_all(open("ecommerce-mappings-1.2.yaml")))
source = yaml.safe_load_all(open("ecommerce-cards-1.21-en.yaml"))
opencre_base_url = "http://www.opencre.org/rest/v1"


def get_standard_page(page, standard_name, standard_to_cre):
    url = f"{opencre_base_url}/standard/{standard_name}?page={page}"
    resp = requests.get(url)
    if resp.status_code == 200:
        body = resp.json()
        results = body.get("standards")
        if len(results) > 0:
            for standard in body.get("standards"):
                section = standard.get("section")
                if "links" in standard:
                    cres = [
                        link.get("document").get("id")
                        for link in standard.get("links")
                        if link.get("document").get("doctype") == "CRE"
                    ]
                    if cres:
                        standard_to_cre[section] = cres
                    else:
                        pprint(
                            f"{standard_name} {section} has links that aren't cre? looks like a bug!"
                        )
                        pprint(body)
                else:
                    pprint(f"{standard_name} {section} not linked yet, chase spyros")
                    standard_to_cre[section] = []
                    # return
        else:
            pprint(f"opencre.org is not aware of {standard_name} yet, chase spyros")
            standard_to_cre[standard.get("section")] = []
    return standard_to_cre


def remove_last_digit(s):
    return re.sub("^V", "", re.sub(r"(\.\d+)$", "", s))


def get_cres_based_on_standard(standard_name):
    standard_to_cre = {}
    url = f"{opencre_base_url}/standard/{standard_name}?page=1"
    resp = requests.get(url)
    if resp.status_code == 200:
        body = resp.json()
        total_pages = body.get("total_pages")
        for page in range(0, total_pages):
            standard_to_cre = get_standard_page(page, standard_name, standard_to_cre)
    return standard_to_cre


capec_to_cres = get_cres_based_on_standard("CAPEC")

# cornucopia specific part, ASVS in cornucopia is mapped only to section, we map subsections

card_val_to_desc = {}
for src in source:
    for suit in src.get("suits"):
        name = suit.get("name")
        card_val_to_desc[name] = {}
        for card in suit.get("cards"):
            card_val_to_desc[name][card.get("value")] = card.get("desc")

result = mappings.copy()
for index, m in enumerate(mappings):
    for suitsIndex, mapping in enumerate(m.get("suits")):
        name = mapping.get("name")
        for cardIndex, card in enumerate(mapping.get("cards")):

            my_set = set()
            # res = [asvs_to_cres.get(f"{asvs}") for asvs in card.get("owasp_asvs") if  asvs_to_cres.get(f"{asvs}") ]
            res2 = []
            # if not res:
            # pprint(f"could not find asvs {[asvs for asvs in card.get('owasp_asvs')]}")
            res2 = [
                capec_to_cres.get(f"{capec}")
                for capec in card.get("capec")
                if capec_to_cres.get(f"{capec}")
            ]
            if not len(res2):
                pprint(f"could not find capec {[capec for capec in card.get('capec')]}")
                pprint(
                    f"for manual mapping card is {card_val_to_desc[name][card.get('value')]}"
                )
                pprint("-------------------")

            my_set = set(itertools.chain.from_iterable(res2))
            result[index]["suits"][suitsIndex]["cards"][cardIndex]["cre"] = list(my_set)
            result[index]["suits"][suitsIndex]["cards"][cardIndex]["description"] = card_val_to_desc[name][card.get("value")]

with open("./cre-mappings-1.2.yaml", "w") as outf:
    yaml.safe_dump_all(result, outf, default_flow_style=None, explicit_start=True)
