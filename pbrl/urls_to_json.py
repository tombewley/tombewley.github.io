import json

FNAME = "frosty-jazz-9"

with open(f"{FNAME}.raw", "r") as f:
    lines = f.read()

urls = []
while True:
    idx = lines.find("[IMG]")
    if idx == -1:
        break
    lines = lines[lines.find("[IMG]") + 5 :]
    urls.append(lines[: lines.find("[/IMG]")])

with open(f"{FNAME}.json", "w") as f:
    json.dump(urls, f, indent=4)
