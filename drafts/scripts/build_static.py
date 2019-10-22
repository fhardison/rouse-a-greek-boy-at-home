#!/usr/bin/env python3

import glob
import os
import re
import mistletoe


def make_line_num(num):
    return f"""<label for="ln-{num}" class="margin-toggle"></label>
<input type="checkbox" id="ln-{num}" class="margin-toggle"/>
<span class="marginnote"><i>{num}</i></span>"""

def convert_line_numbers(line, line_count):
    line_nums = re.findall(r'\{(\d*\.?\d+)\}', line)
    print(line_nums)
    if not(line_nums):
        return (line, line_count)
    lcount = line_count
    for line_num in line_nums:
        #handle line numbers
        if '.' in line_num:
            if line_num[0] == '.':
                lcount = int(line_num.replace('.', ''))
            else:
                _, lcount = line_num.split('.')
            line = line.replace("{" + str(line_num)+ "}",make_line_num(line_count + lcount))
        #remove page refs
        else:
            line = line.replace("{" + str(line_num)+ "}",'')
            print(line_count)
            line_count += lcount
    return (line, line_count)

def make_title(raw):
    return raw.replace('greek-boy-ch', 'Chapter ').replace('.md', '').replace("..\\..\\src\\", '')


WORK_LIST = glob.glob(os.path.join('..','..', 'src', '*.md')) #['greek-boy-ch03.md']

for WORK in WORK_LIST:
    print(WORK)
    SRC = WORK
    DEST = WORK.replace("src", "docs").replace(".md", ".html")
    TITLE = 'A Greek Boy at Home, ' + make_title(SRC)
    HEADER = f"""\
    <!DOCTYPE html>
    <html lang="grc">
    <head>
    <title>{TITLE}</title>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css?family=Noto+Serif:400,700&amp;subset=greek,greek-ext" rel="stylesheet">
    <link href="tufte.min.css" rel="stylesheet">

    </head>
    <body>
      <article>
      <nav>&#x2191; <a href="http://fhardison.github.io/rouse-a-greek-boy-at-home/">Rouse's A Greek Boy at Home</a></nav>
      <h1 lang="en">{TITLE}</h1>
      <section>
    """

    FOOTER = """\
    </section>
      </article>
    </body>
    </html>
    """

    with open(SRC, encoding="UTF-8") as f:
        with open(DEST, "w", encoding="UTF-8") as g:
            prev_contents = None
            print(HEADER, file=g)
            line_counter = 0
            for line in f:
                parts = line.strip().split(maxsplit=1)
                ref = parts[0].split(".")
                contents = parts[1]
                #handle headers
                if "#" in contents:
                    if prev_contents:
                        if prev_contents.count('#') == contents.count('#'):
                            prev_contents = prev_contents + "<br/>" + contents.replace('#', '')
                        else:
                            prev_contents = contents
                    else:
                        if prev_contents:
                            header_lvl = prev_contents.count('#')
                            print(f"<h{header_lvl}>{prev_contents.replace('#', '').strip()}</h{header_lvl}>", file=g)
                            header_lvl = None
                        prev_contents = contents
                #handle content
                else:
                    #actualy typeset headers
                    if prev_contents:
                        header_lvl = prev_contents.count('#')
                        print(f"<h{header_lvl}>{prev_contents.replace('#', '').strip()}</h{header_lvl}>", file=g)
                        header_lvl = None
                    #convert line numbers
                    contents, line_counter = convert_line_numbers(contents, line_counter)
                    print(f"{mistletoe.markdown(contents)}", file=g)
                    prev_contents = None
            print(FOOTER, file=g)
print("Done!")
