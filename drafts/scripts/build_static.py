#!/usr/bin/env python3

import glob
import os
import re
import mistletoe


class Renderer():
    def render(self, ref, cons):
        pass


class StaticRenderer():
    def __init__(self):
        self.renderers = {}
        self.buffers = {}
        self.patterns = []
        self.line_renderers = []

    def add_renderer(self, pattern, f):
        self.buffers[pattern] = []
        self.renderers[pattern] = f
        self.patterns.append(pattern)

    def add_line_renderer(self, f):
        self.line_renderers.append(f)

    def add_if_buffer(self, ref):
        for pattern in self.patterns:
            if pattern in ref:
                self.buffers[pattern].append(ref)

    def render_buffers(self, cons):
        for key, buffer in self.buffers.items():
            renderer = self.renderers[key]
            for ref in buffer:
                renderer.render(ref, cons)
        self.clear_buffers()

    def render_lines(self, cons, printf):
        for line in cons:
            for renderer in self.line_renderers:
                line = renderer.render("", line)
            printf(line)

    def clear_buffers(self):
        self.buffers = {}

class LineNumberRenderer(Renderer):
    def __init__(self):
        self.line_counter = 0

    def make_margin_note(self, id, content, css_class='', marker=''):
        return f"""<label for="ln-{id}" class="margin-toggle {css_class}">{marker}</label>
                    <input type="checkbox" id="ln-{id}" class="margin-toggle"/>
                    <span class="marginnote">{content}</span>"""

    def make_line_num(self, num):
        return self.make_margin_note(num, f"<i>{num}</i>")


    def render(self, ref, line):
        line_nums = re.findall(r'\{(\d*\.?\d+)\}', line)
        print(line_nums)
        if not(line_nums):
            return line
        for line_num in line_nums:
            #handle line numbers
            if '.' in line_num:
                self.line_counter += 5
                line = line.replace("{" + str(line_num)+ "}", self.make_line_num(self.line_counter))
            #remove page refs
            else:
                line = line.replace("{" + str(line_num)+ "}",'')

        return line.replace('  ', ' ') #clean up any double spaces left by line/page num markers

class HeaderRenderer(Renderer):
    def render(self, ref, cons):
        if "#" in cons:
            header_lvl = cons.count('#')
            return f"<h{header_lvl}>{cons.replace('#', '').strip()}</h{header_lvl}>"
        else:
            return cons

class SideNoteRenderer(Renderer):
    def make_margin_note(self, id, content, css_class='', marker=''):
        return f"""<label for="ln-{id}" class="margin-toggle {css_class}">{marker}</label>
    <input type="checkbox" id="ln-{id}" class="margin-toggle"/>
    <span class="marginnote">{content}</span>"""

    def make_line_num(self, num):
        return self.make_margin_note(num, f"<i>{num}</i>")

    def make_sidenote(self, line, fn_content, fn_num):
        return line.replace(f" [{fn_num}]",
            self.make_margin_note(fn_num, fn_content, css_class='sidenote-number'), 1)
            # only make one replacement in case of multiple fns with same fn_num
            #  which should not happen, but who knows

    def render(self, ref, cons):
        ref_parts = ref.split('.')
        fn_num = ref_parts[-1]
        ref_num = '.'.join(ref_parts[:-1])
        cons[ref_num] = self.make_sidenote(cons[ref_num], cons[ref], fn_num)
        del cons[ref] #remove FN after processing

renderer = StaticRenderer()

renderer.add_renderer("fn", SideNoteRenderer())
renderer.add_line_renderer(LineNumberRenderer())
renderer.add_line_renderer(HeaderRenderer())


def make_title(raw):
    return raw.replace('greek-boy-ch', 'Chapter ').replace('.md', '').replace(os.path.join("..", "..", "src") + "/", '')


WORK_LIST = glob.glob(os.path.join('..','..', 'src', '*.md'))

for WORK in WORK_LIST:
    print(WORK)
    SRC = WORK
    DEST = WORK.replace("src", "docs").replace(".md", ".html")
    TITLE = 'A Greek Boy at Home, ' + make_title(SRC)
    print(TITLE)
    HEADER = f"""
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
                    renderer.add_if_buffer(ref)
                    cons[ref] = content
                else:
                    print("Multiple lines with same ref number in file!")
            renderer.render_buffers(cons)
            print(len(cons))
            renderer.render_lines(list(cons.values()), lambda x: print(f"{mistletoe.markdown(x)}", file=g))
            print(FOOTER, file=g)
print("Done!")
