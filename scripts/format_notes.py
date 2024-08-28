import os


COLLECTIONS = {
    "./_notes": "notes",
}

for root, subdirs, files in os.walk("."):
    if root in COLLECTIONS:
        for file in files:
            # print(file)
            file_path = f"{root}/{file}"

            with open(file_path, "r") as f:
                string = f.read()

            if string.startswith("---"):
                string_new = ""
                add_fm = False
            else:
                title = file_path.split("/")[-1][:-3]
                collection = COLLECTIONS[root]
                string_new = f"---\ntitle: {title}\npermalink: /{collection}/{title}\ncollection: {collection}\n---\n"
                add_fm = True

            s = 0
            n_conv = 0
            n_ext = 0
            while s < len(string) - 2:
                if string[s : s + 2] == "[[":
                    # Convert WikiLinks to MDLinks
                    found = False
                    for e in range(s + 2, len(string)):
                        if string[e : e + 2] == "]]":
                            split = string[s + 2 : e].split("|")
                            assert len(split) <= 2, split
                            string_new += (
                                f"[{split[-1]}]({split[0].replace(' ', '%20')})"
                            )
                            s += e + 2 - s
                            found = True
                            n_conv += 1
                            break
                    if not found:
                        raise Exception(f"Unclosed WikiLink in {file_path}")
                else:
                    # Remove .md extension from MDLinks
                    if string[s : s + 4] == ".md)":
                        s += 3
                        n_ext += 1
                    string_new += string[s]
                    s += 1

            string_new += string[s:]
            if n_conv:
                print(f"Converted {n_conv} WikiLinks to MDLinks in {file_path}")
            if n_ext:
                print(f"Removed {n_ext} .md MDLink extensions in {file_path}")

            if add_fm or n_conv or n_ext:
                with open(file_path, "w") as f:
                    f.write(string_new)
