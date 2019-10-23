#!/usr/bin/env python3

import glob
import os
import re
import mistletoe



def make_margin_note(id, content, css_class='', marker=''):
    return f"""<label for="ln-{id}" class="margin-toggle {css_class}">{marker}</label>
<input type="checkbox" id="ln-{id}" class="margin-toggle"/>
<span class="marginnote">{content}</span>"""

def make_line_num(num):
    return make_margin_note(num, f"<i>{num}</i>")

def make_sidenote(line, fn_content, fn_num):
    return line.replace(f" [{fn_num}]",
        make_margin_note(fn_num, fn_content, css_class='sidenote-number'), 1)
        # only make one replacement in case of multiple fns with same fn_num
        #  which should not happen, but who knows



def convert_line_numbers(line, line_count):
    line_nums = re.findall(r'\{(\d*\.?\d+)\}', line)
    print(line_nums)
    if not(line_nums):
        return (line, line_count)
    for line_num in line_nums:
        #handle line numbers
        if '.' in line_num:
            line_count += 5
            line = line.replace("{" + str(line_num)+ "}", make_line_num(line_count))
        #remove page refs
        else:
            line = line.replace("{" + str(line_num)+ "}",'')

    return (line.replace('  ', ' '), line_count) #clean up any double spaces left by line/page num markers

def make_title(raw):
    return raw.replace('greek-boy-ch', 'Chapter ').replace('.md', '').replace("..\\..\\src\\", '')


WORK_LIST = glob.glob(os.path.join('..','..', 'src', '*.md'))

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
            print(HEADER, file=g)
            line_counter = 0
            cons = dict()
            fn_buffer = []
            for line in f:
                parts = line.strip().split(maxsplit=1)
                ref = parts[0]
                content = parts[1]
                if not(content in cons):
                    if "fn" in ref:
                        fn_buffer.append(ref)
                    cons[ref] = content
                else:
                    print("Multiple lines with same ref number in file!")
            for fn in fn_buffer:
                ref_parts = fn.split('.')
                fn_num = ref_parts[-1]
                ref_num = '.'.join(ref_parts[:-1])
                cons[ref_num] = make_sidenote(cons[ref_num], cons[fn], fn_num)
                del cons[fn] #remove FN after processing
            for ref, content in cons.items():
                #handle headers
                if "#" in content:
                    header_lvl = content.count('#')
                    print(f"<h{header_lvl}>{content.replace('#', '').strip()}</h{header_lvl}>", file=g)
                #handle content
                else:
                    #convert line numbers
                    content, line_counter = convert_line_numbers(content, line_counter)
                    print(f"{mistletoe.markdown(content)}", file=g)
            print(FOOTER, file=g)
print("Done!")
