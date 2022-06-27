from collections import defaultdict
import re
import markdown


IFILE = '.\\src\\rouse_text.txt'
OFILE = '.\\docs\\index.html'


# read_file to section : paragraph : sentence

DATA = defaultdict( lambda: defaultdict(dict))

with open(IFILE,  'r', encoding="UTF-8") as f:
    for line in f:
        if not line.strip():
            continue
        ref, cons = line.strip().split(' ', maxsplit=1)
        section, paragraph, sentence  = ref.replace('.text', '').split(".", maxsplit=2)
        DATA[section][paragraph][sentence] = cons
    
print(len(DATA.items()))   

HEADER = """<!DOCTYPE html>
<html lang="grc">
  <head>
    <title>Greek Boy at Home</title>
    <meta charset="utf-8">
    <link href="default.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/alpheios-components@latest/dist/style/style-components.min.css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

  </head>
  <body class="default">
    <div class="container alpheios-enabled" lang="grc">"""

FOOTER = """</div>
    <script type="text/javascript">
      document.addEventListener("DOMContentLoaded", function(event) {
      import ("https://cdn.jsdelivr.net/npm/alpheios-embedded@latest/dist/alpheios-embedded.min.js").then(embedLib => {
          window.AlpheiosEmbed.importDependencies({ 
          mode: 'cdn'
          }).then(Embedded => {
          new Embedded({clientId: "thrax-grammar-fhard"}).activate();
          }).catch(e => {
          console.error(`Import of Alpheios embedded library dependencies failed: ${e}`)
          })

      }).catch(e => {
          console.error(`Import of Alpheios Embedded library failed: ${e}`)
      })
      });
  </script>
  </body>
</html>"""

def do_markdown(sent):
    text = markdown.markdown(sent)

    return text.replace('<p>', '').replace('</p>', '').replace("\\'", "'")
    # if '*' in sent:
    #     sent = re.sub(r'(\w)\*', r'\1</em>',  sent)
    #     sent = re.sub(r'\*(\w)', r'<em>\1',  sent)

    # if '**' in sent:
    #     sent = re.sub(r'(\w)\*\*', r'\1</strong>',  sent)
    #     sent = re.sub(r'\*\*(\w)', r'<strong>\1',  sent)
    
    # if sent.startswith('> '):
    #     sent = '<blockquote>' + sent.replace('>', '') + "</blockquote>"
    # elif sent.strip() == '>':
    #     sent = '<blockquote>' + sent.replace('>', '') + "</blockquote>"
    
    # return sent

with open('.\\docs\\greekboy.html', 'w', encoding='UTF-8') as g:
    print(HEADER, file=g)
    for section in DATA.values():
        for paragraph in section.values():
            if '0' in paragraph:
                if re.findall(r'[α-ζΑ-Ζ]', paragraph['0']):
                    print("""<div class="section">
  <h3 class="section-title">""" + paragraph['0'].replace('#', '').replace("*", '').strip() + '</h3>', file=g)

                else:
                    print("""<div class="section">
  <h2 class="section-title">""" + paragraph['0'].replace('#', '').replace("*", '').strip() + '</h2>', file=g)
                del paragraph['0']
            print('<div class="paragraph">', file=g)
            for sentence in paragraph.values():
                print('<div class="sentence">' + do_markdown(sentence) + '</div>', file=g)
            print("</div>", file=g)
        print("</div>", file=g)
    print(FOOTER, file=g)
         