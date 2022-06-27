from re import sub, findall

IFILE = '.\\drafts\\2_working_rouse.md'


# desired output format
# section.paragraph.sentence
#

SECTION = 0
SUBSECTION = 0
PARAGRAPH = 0
LINE = 0

CHUNKS = []

with open(IFILE, 'r', encoding="UTF-8") as f, open('.\\src\\rouse_text.txt', 'w', encoding="UTF-8") as g:
    buffer = []
    for line in f:
        if not line.strip():
            if not buffer == []:
                CHUNKS.append(' '.join(buffer))
                buffer = []
        else:
            buffer.append(line.strip())
    CHUNKS.append(' '.join(buffer))
    
    for line in CHUNKS:
        # section heading
        print(findall(r'[ΙXV0-9]+', line))
        if (findall(r'[ΙVX0-9]+', line) and '**' in line) or '##' in line:
            SECTION += 1
            PARAGRAPH = 0
            LINE = 0
            print(f"{SECTION}.{PARAGRAPH}.{LINE}.text # {line.strip().replace('#', '')}", file=g)
        elif '>' in line:
            PARAGRAPH += 1
            LINE = 0
            for sentence in line.split("> "):
                s = sentence.replace("\\'", "'").replace('\\"', '"').strip()
                if s == '':
                    continue
                LINE += 1
                print(f"{SECTION}.{PARAGRAPH}.{LINE}.text > {s}", file=g)
        else:
            if not line.strip():
                continue
            PARAGRAPH += 1
            sentences = [x for x in sub(r'([.?!][^*])', r'\1@@@', line.strip()).split('@@@') if x.strip()]
            LINE = 0
            for sentence in sentences:
                LINE += 1
                s = sentence.replace("\\'", "'").replace('\\"', '"').strip()
                print(f"{SECTION}.{PARAGRAPH}.{LINE}.text {s}", file=g)
            print('', file=g)


# Each line is either a heading, or a paragraph
#
# split paragraphs by [.?!] to get sentences
#
#


