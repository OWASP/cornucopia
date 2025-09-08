# This script converts the JSON from
# OWASP_Application_Security_Verification_Standard_5.0.0_en.json
# to the file structure that our cornucopia website can understand.
import shutil
import json
import os

mypath = "../../data/taxonomy/en/ASVS-5.0"


def createLevelSummary(level, arr):
    topic = ""
    category = ""
    os.mkdir(mypath + f"/level-{level}-controls")
    f = open(mypath + f"/level-{level}-controls/index.md", "w", encoding="utf-8")
    f.write(f"# Level {level} controls\r\n\r\n")
    f.write(f"Level {level} contains {len(arr)} controls listed below: \r\n\r\n")
    for link in arr:
        if link["topic"] != topic:
            topic = link["topic"]
            f.write(f"## {topic}\r\n\r\n")
        if link["cat"] != category:
            category = link["cat"]
            f.write(f"### {category}\r\n\r\n")
        shortdesc = link["description"].replace("Verify that", "").strip().capitalize()[0:50] + " ..."
        f.write(f"- [{link['name']}]({link['link']}) *{shortdesc}* \r\n\r\n")
    f.close()


def createASVSPages(data):
    L1 = []
    L2 = []
    L3 = []

    for i in data["Requirements"]:
        name = str(i["Ordinal"]).rjust(2, "0") + "-" + i["Name"].lower().replace(" ", "-").replace(",", "")
        print(name)
        os.mkdir(mypath + "/" + name)
        for item in i["Items"]:
            itemname = (
                str(item["Ordinal"]).rjust(2, "0") + "-" + item["Name"].lower().replace(" ", "-").replace(",", "")
            )
            print(item)
            thispath = mypath + "/" + name + "/" + itemname
            os.mkdir(thispath)
            print("🟩")
            f = open(thispath + "/index.md", "w")
            f.write("# " + item["Name"].replace(",", ""))
            f.write("\r\n")
            for subitem in item["Items"]:
                f.write("## " + subitem["Shortcode"] + "\r\n")
                f.write(subitem["Description"].encode("ascii", "ignore").decode("utf8", "ignore") + "\r\n")
                if int(subitem["L"]) == 1:
                    f.write("Required for Level 1, 2 and 3\r\n")
                if int(subitem["L"]) == 2:
                    f.write("Required for Level 2 and 3\r\n")
                if int(subitem["L"]) == 3:
                    f.write("Required for Level 3\r\n")
                shortcode = subitem["Shortcode"]
                description = subitem["Description"]
                link = f"/taxonomy/asvs-5.0/{name}/{itemname}#{shortcode}"
                obj = {
                    "topic": name,
                    "cat": itemname,
                    "name": shortcode,
                    "link": link,
                    "description": description,
                }
                if int(subitem["L"]) == 1:
                    L1.append(obj)

                if int(subitem["L"]) == 2:
                    L2.append(obj)

                if int(subitem["L"]) == 3:
                    L3.append(obj)

                # cwe = str(subitem["CWE"]).replace("[", "").replace("]", "")
                # f.write("CWE: [" + cwe + "](https://cwe.mitre.org/data/definitions/" + cwe + ")\r\n")
                print("object:")
                print(obj)
                print("🟪")

                print(subitem)
            f.write("## Disclaimer\r\n")
            f.write(
                "Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)."
                "For more information visit: "
                "[The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/)"
                " or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the "
                "[Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md)"
                " license."
            )
            f.write("\n")
            f.close()

    createLevelSummary(1, L1)
    createLevelSummary(2, L2)
    createLevelSummary(3, L3)


def main():
    print("Starting ASVS conversion process")

    try:
        # Empty the folder
        shutil.rmtree(mypath)
    except Exception as e:
        print(e)
    os.mkdir(mypath)
    # Load the JSON
    f = open("OWASP_Application_Security_Verification_Standard_5.0.0_en.json", encoding="utf8")
    data = json.load(f)
    createASVSPages(data)

    print("DONE")


main()
