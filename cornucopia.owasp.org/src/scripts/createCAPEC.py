# This script converts the JSON from
# data/capec-3.9/3000.json
# to the file structure that our cornucopia website can understand.
import shutil
import json
import os
from pathlib import Path

mypath = "../../data/taxonomy/en/CAPEC-3.9"

def createCAPECPages(data):
    directory = Path(__file__).parent.resolve()
    for i in data["Attack_Pattern"]:
        name = str(i["_ID"])
        
        capecPath = directory / mypath / name
        print("Create: " + str(capecPath))
        if not os.path.exists(capecPath):
            os.makedirs(capecPath)

        f = open(capecPath / "index.md", "w", encoding="utf-8")
        f.write(f"# CAPEC-{i['_ID']}: {i['_Name']}\r\n")
        f.write("## Description\r\n")
        
        description = i["Description"]
        if isinstance(i["Description"], dict) and "Description" in i and "p" in i["Description"]:
            if isinstance(i["Description"]["p"], dict) and "__text" in i["Description"]["p"]:
                description = i["Description"]["p"]["__text"]
            elif isinstance(i["Description"]["p"], list):
                description = " ".join([p["__text"] if isinstance(p, dict) and "__text" in p else str(p) for p in i["Description"]["p"]])

        f.write(f"{description}\r\n")
        f.write(f"Source: [CAPEC-{i['_ID']}](https://capec.mitre.org/data/definitions/{i['_ID']}.html)\r\n")
        f.close()

def main():
    print("Starting ASVS conversion process")
    directory = Path(__file__).parent.resolve()
    try:
        # Empty the folder
        shutil.rmtree(mypath)
    except Exception as e:
        print(e)
    if not os.path.exists(os.path.dirname(directory / mypath)):
        os.mkdir(directory / mypath)
    
    # Load the JSON
    
    f = open(directory / "../../data/capec-3.9/3000.json", encoding="utf8")
    data = json.load(f)
    createCAPECPages(data["Attack_Pattern_Catalog"]["Attack_Patterns"])

    print("DONE")


main()