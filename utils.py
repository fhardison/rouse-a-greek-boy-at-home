import os
import shutil

from jinja2 import Environment, ChoiceLoader, FileSystemLoader
from roman_numerals import convert_to_numeral


def relative_to_absolute(base, rel):
    return os.path.abspath(os.path.join(os.path.dirname(base), rel))

def absolute_directory(filename):
    return os.path.abspath(os.path.dirname(filename))

def create_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print(f"created {dirname}")


def copy_file(input_filename, output_dir):
    output_filename = os.path.join(output_dir, os.path.basename(input_filename))
    shutil.copy(input_filename, output_filename)
    print(f"copied {output_filename}")


def roman(s):
    if s.isnumeric():
        return convert_to_numeral(int(s))
    else:
        return s


def load_template(template_name, extra_dir):
    env = Environment(
        loader=ChoiceLoader([
            FileSystemLoader(os.path.join(extra_dir, "templates")),
            FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
        ]),
    )
    env.filters["roman"] = roman
    return env.get_template(template_name)


def render(template_filename, context, output_filename, extra_dir):
    with open(output_filename, "w", encoding="UTF-8") as output:
        template = load_template(template_filename, extra_dir)
        print(template.render(**context), file=output)
    print(f"rendered {output_filename}")


def build_tree(filename, title, levels):

    root = {
        "title": title,
        "kind": "work",
        "children": {},
    }

    with open(filename, encoding="UTF-8") as f:

        for line in f:
            parts = line.strip().split(maxsplit=1)
            ref = parts[0].split(".")

            node = root
            for level, ref_part in zip(levels[:-1], ref[:-1]):
                node = node["children"].setdefault(ref_part, {
                    "kind": level,
                    "children": {},
                })

            node["children"][ref[-1]] = {
                "kind": levels[-1],
                "content": parts[1],
            }

    return root
