from bs4 import BeautifulSoup



XMLFILE = "greekboy.xml"


raw = None
with open(XMLFILE, 'r', encoding="UTF-8") as f:
	raw = f.read()
	#indata = re.sub(r'<(\w+)\s*style="ddg"\s*closed="false"\s*>', r'<\1 style="ddg"></\1>', raw)
	#with open('tempStep.xml', 'w', encoding="UTF-8") as o:
	#	o.write(indata)

soup = BeautifulSoup(raw, 'html.parser')

chapters = soup.body.find_all('div', attrs={'class': 'chap'})

print(chapters[0]['id'])

def replaceSections(chapter):
	sects = chapter.find_all("div", attrs={"class" : 'sect'})
	for s in sects:
		s.h2.string = "## " + s.h2.text.replace("\n", " --- ") + "\n"


def saveChapter(chapter):
	filename = "greek-boy-" + chapter['id'] + ".md"
	chapter.h2.string = "# " + chapter.h2.text.replace("\n", " --- ") + "\n"
	replaceSections(chapter)
	with open(filename, 'w', encoding='UTF-8') as f:
		f.write(chapter.text)


for chapter in chapters:
    saveChapter(chapter)

print("done!")
