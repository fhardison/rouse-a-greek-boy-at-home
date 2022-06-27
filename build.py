#!/usr/bin/env python3

import json
import sys

from utils import create_dir, copy_file, render, build_tree, relative_to_absolute, absolute_directory

CONFIG_FILE = sys.argv[1]

config = json.load(open(CONFIG_FILE))

SRC_PATTERN = config["SRC_PATTERN"]
OUTPUT_DIRECTORY = config["OUTPUT_DIRECTORY"]
if not OUTPUT_DIRECTORY.endswith("/"):
    OUTPUT_DIRECTORY += "/"
DST_PATTERN = f"{OUTPUT_DIRECTORY}{{source}}.html"

output_dir = relative_to_absolute(CONFIG_FILE, OUTPUT_DIRECTORY)

create_dir(output_dir)
copy_file(relative_to_absolute(__file__, "css/default.css"), output_dir)

for filename in config.get("EXTRA_FILES", []):
    copy_file(relative_to_absolute(CONFIG_FILE, filename), output_dir)


for work in config["works"]:
    SRC = relative_to_absolute(CONFIG_FILE, SRC_PATTERN.format(**work))
    DST = relative_to_absolute(CONFIG_FILE, DST_PATTERN.format(**work))

    render("page.html", {
        "node": build_tree(SRC, work["title"], work["levels"]),
        "collection": config["collection"],
    }, DST, absolute_directory(CONFIG_FILE))


render("index.html", {
    "works": [
        {
            "link": f"./{work['source']}.html",
            "title": work["title"],
        }
        for work in config["works"]
    ],
    "collection": config["collection"],
    "subtitle": config["subtitle"],
    "repo_link": config.get("repo_link"),
}, relative_to_absolute(CONFIG_FILE, f"{OUTPUT_DIRECTORY}/index.html"), absolute_directory(CONFIG_FILE))


