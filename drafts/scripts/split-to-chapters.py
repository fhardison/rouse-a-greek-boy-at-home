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


def reformat_page_and_line_numbers(chapter, page, line):
	def process_p_tag(p, page, line):
		# check for footnotes
		try:
			if 'fn' in p['class']:
				return page, line
		except KeyError:
			pass

		new_lines = []
		for child in p.children:
			# print(child)

			if child.name == 'span':
				# found a page number
				page = child['id'].strip('p')
				child.string = ''
				line = 1
			elif child.name == 'a':
				# link to a footnote, do nothing but save the text
				new_lines.append(child.string)
				continue
			else:
				# must be plain text, divide into lines by line break
				if child.string is None:
					continue
				lines = child.string.split('\n')
				for l in lines:
					# ignore empty lines
					if l == '':
						continue
					l2 = f'{{{page}.{line}}} ' + l
					line = line + 1
					new_lines.append(l2)

		# collect parsed data for this p tag
		p.string = ' '.join(new_lines)
		return page, line

	def process_span_tag(span):
		page = span['id'].strip('p')
		line = 1
		return page, line

	for tag in chapter.children:
		if tag.name == 'span':
			page, line = process_span_tag(tag)
		elif tag.name == 'p':
			page, line = process_p_tag(tag, page, line)

		else:
			# ignore illustrations
			if tag.name == 'div' and 'ill' in tag['class']:
				continue

			try:
				for child in tag.children:
					if child.name == 'span':
						page, line = process_span_tag(child)
					elif child.name == 'p':
						page, line = process_p_tag(child, page, line)
					# 2nd level divs are poetry lines
					elif child.name == 'div':
						page, line = process_p_tag(child, page, line)
			except AttributeError:
				pass

	return page, line


def save_chapter(chapter, page, line):
	filename = "greek-boy-" + chapter['id'] + ".md"
	chapter.h2.string = "# " + chapter.h2.text.replace("\n", " --- ") + "\n"
	replace_sections(chapter)
	page, line = reformat_page_and_line_numbers(chapter, page, line)
	reformat_paragraphs(chapter)
	clean_text = strip_extra_blank_lines(chapter)
	with open(filename, 'w', encoding='UTF-8') as f:
		f.write(clean_text)
	return page, line


XMLFILE = "greekboy.xml"

raw = None
with open(XMLFILE, 'r', encoding='UTF-8') as f:
	raw = f.read()
	# indata = re.sub(r'<(\w+)\s*style="ddg"\s*closed="false"\s*>', r'<\1 style="ddg"></\1>', raw)
	# with open('tempStep.xml', 'w', encoding="UTF-8") as o:
	# 	o.write(indata)

soup = BeautifulSoup(raw, 'html.parser')

page = 1
line = 1
chapters = soup.body.find_all('div', attrs={'class': 'chap'})
for chapter in chapters:
	page, line = save_chapter(chapter, page, line)

print("done!")
	
