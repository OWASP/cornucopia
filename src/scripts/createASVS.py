# This script converts the JSON from https://github.com/OWASP/ASVS/blob/master/4.0/docs_en/OWASP%20Application%20Security%20Verification%20Standard%204.0.3-en.json
# to the file structure that our cornucopia website can understand.
import shutil
from os import walk
import json
import os 

mypath = "../../data/taxonomy/ASVS-4.0.3"



def createLevelSummary(level,arr):
    topic = ""
    category = ""
    os.mkdir(mypath + f'/level-{level}-controls')
    f = open(mypath + f'/level-{level}-controls/index.md', "w")
    f.write(f"# Level {level} controls\r\n")
    f.write(f"Level {level} contains {len(arr)} controls listed below: \r\n")
    for link in arr:
        if(link['topic'] != topic):
            topic = link['topic']
            f.write(f"## {topic}\r\n")
        if(link['cat'] != category):
            category = link['cat']
            f.write(f"### {category}\r\n")
        shortdesc = link['description'].replace("Verify that","").strip().capitalize()[0:50] + ' ...'
        f.write(f"- [{link['name']}]({link['link']}) *{shortdesc}* \r\n")
    f.close()

def main():
    print("Starting ASVS conversion process")

    try:
        # Empty the folder 
        shutil.rmtree(mypath)
    except: 
        print("exception")
    os.mkdir(mypath) 
    # Load the JSON
    f = open('OWASP Application Security Verification Standard 4.0.3-en.json',encoding="utf8")
    data = json.load(f)

    L1 = [];
    L2 = [];
    L3 = [];

    for i in data['Requirements']:
        name = str(i['Ordinal']).rjust(2,"0") + '-' + i['Name'].lower().replace(" ","-").replace(",","")
        print(name);
        os.mkdir(mypath + '/' + name) 
        for item in i['Items']:
            itemname = str(item["Ordinal"]).rjust(2,"0") + '-' + item["Name"].lower().replace(" ","-").replace(",","")
            print(itemname)
            print(item)
            thispath = mypath + '/' + name + '/' + itemname
            os.mkdir(thispath)
            print("🟩")
            f = open(thispath + '/index.md', "w")
            f.write("#  " + item["Name"].replace(",",""))
            f.write("\r\n")
            for subitem in item["Items"]:
                f.write("## " + subitem["Shortcode"] + "\r\n")
                f.write(subitem["Description"].encode("ascii","ignore").decode("utf8","ignore") + "\r\n")
                f.write("Level 1 required: " + str(subitem["L1"]["Required"]) + "\r\n")
                f.write("Level 2 required: " + str(subitem["L2"]["Required"]) + "\r\n")
                f.write("Level 3 required: " + str(subitem["L3"]["Required"]) + "\r\n")
                shortcode = subitem["Shortcode"]
                description = subitem["Description"]
                link = f"/taxonomy/ASVS-4.0.3/{name}/{itemname}#{shortcode}"
                obj = {
                    'topic'  : name,
                    'cat'  : itemname,
                    'name' : shortcode,
                    'link' : link,
                    'description' : description,
                }
                if(subitem["L1"]["Required"]):
                    L1.append(obj)

                if(subitem["L2"]["Required"]):
                    L2.append(obj)

                if(subitem["L3"]["Required"]):
                    L3.append(obj)

                cwe = str(subitem["CWE"]).replace("[","").replace("]","")
                f.write("CWE: [" + cwe + "](https://cwe.mitre.org/data/definitions/" + cwe + ")\r\n")
                print("🟪")
                print(subitem)
            f.write("\r\n")
            f.write("## Disclaimer:\r\n")
            f.write("Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.")
            f.write("\r\n")
            f.close()

    createLevelSummary(1,L1)
    createLevelSummary(2,L2)
    createLevelSummary(3,L3)

    print("DONE")

main()