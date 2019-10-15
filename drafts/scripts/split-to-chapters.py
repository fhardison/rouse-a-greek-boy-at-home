import re
from bs4 import BeautifulSoup


def replace_sections(chapter):
	sects = chapter.find_all("div", attrs={"class": 'sect'})
	for s in sects:
		s.h2.string = "## " + s.h2.text.replace("\n", " --- ") + "\n"


def reformat_paragraphs(chapter):
	for p in chapter.find_all('p'):
		p.string = p.text.replace('\n', ' ') + '\n'


def strip_extra_blank_lines(chapter):
	return re.sub(r'\n\s*\n', '\n\n', chapter.text)


def save_chapter(chapter):
	filename = "greek-boy-" + chapter['id'] + ".md"
	chapter.h2.string = "# " + chapter.h2.text.replace("\n", " --- ") + "\n"
	replace_sections(chapter)
	reformat_paragraphs(chapter)
	clean_text = strip_extra_blank_lines(chapter)
	with open(filename, 'w', encoding='UTF-8') as f:
		f.write(clean_text)


XMLFILE = "greekboy.xml"

raw = None
with open(XMLFILE, 'r', encoding="UTF-8") as f:
	raw = f.read()
	# indata = re.sub(r'<(\w+)\s*style="ddg"\s*closed="false"\s*>', r'<\1 style="ddg"></\1>', raw)
	# with open('tempStep.xml', 'w', encoding="UTF-8") as o:
	# 	o.write(indata)

soup = BeautifulSoup(raw, 'html.parser')

chapters = soup.body.find_all('div', attrs={'class': 'chap'})
for chapter in chapters:
	save_chapter(chapter)

print("done!")
