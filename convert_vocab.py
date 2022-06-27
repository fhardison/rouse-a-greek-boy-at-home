import json

IFILE = '.\\vocab\\vocab.csv'

DATA = []
with open(IFILE, 'r', encoding="UTF-8") as f:
    for line in f:
        if line.strip():
            headword, deff = line.split('\t', maxsplit=1)
            DATA.append({'head': headword.strip(), 'deff':  deff.strip() })

with open('.\\docs\\vocab.js', 'w', encoding="UTF-8") as g:
    json.dump(DATA, g, ensure_ascii=False)