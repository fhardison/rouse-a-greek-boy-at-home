import re, os
from greek_normalisation.utils import (
     nfd, nfc, nfkc,
     strip_accents, count_accents, strip_last_accent, grave_to_acute,
     strip_last_accent_if_two, breathing_check
 )

# just the names of the files. when they are read ".." is prefixed
FILES = ["greek-boy-ch02.md"]



# a check must accept three arguments.
# The word, the line number and the index of that word in the line
# It should return an error message as a string, if a problem is found
# or it should return None to signify that no error is present
def check_breathing_mark(w, line_number, wpos):
    if not(breathing_check(w)):
        return f"\tBreathing mark error on {w} at ({line_number}, {wpos})"
    return None


# It should
# see check_breathing_mark above
CHECKS = [check_breathing_mark]


def read_to_list_of_lines(fpath):
    with open(fpath, 'r', encoding="UTF-8") as f:
        out = []
        i = 1
        for l in f.read().split("\n"):
            out.append((i, l))
            i = i + 1
        return out

def remove_punc(line):
    return re.sub(r'[;\-.–,\'!#’]', '', line)

def apply_checks_to_words(line, checks):
    messages = []
    i, l = line
    words = filter(lambda x: x.strip(), re.split(r'\b', remove_punc(l)))
    for w in words:
        wposition = l.index(w)
        for f in checks:
            result = f(w, i, wposition)
            if result:
                messages.append(result)
    return messages

def check_file(fpath, checks):
    messages = []
    lines = read_to_list_of_lines(fpath)
    for l in lines:
        result = apply_checks_to_words(l, checks)
        if not (result == []):
            messages.extend(result)
    return messages




for FILE in FILES:
    print(FILE)
    messages = check_file(os.path.join("..", FILE), CHECKS)
    if not (messages == []):
        print("\n".join(messages))
