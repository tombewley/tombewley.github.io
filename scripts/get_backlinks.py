import os
import re
import yaml

COLLECTIONS = {
    "./_notes": "notes",
}

REGEX = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

backlinks = {}
for root, subdirs, files in os.walk("."):
    if root in COLLECTIONS:
        for file in files:
            backlinks[file[:-3]] = []

for root, subdirs, files in os.walk("."):
    if root in COLLECTIONS:
        for file in files:
            this_title = file[:-3]

            with open(f"{root}/{file}", "r") as f:
                string = f.read()

            for match in REGEX.findall(string):
                other_title = match[1].replace("%20", " ")
                if other_title in backlinks:
                    backlinks[other_title].append(
                        {"title": this_title, "url": this_title.replace(" ", "%20")}
                    )

# save backlinks to a yaml file in the _data directory

with open("_data/backlinks.yml", "w") as f:
    yaml.dump(backlinks, f)
