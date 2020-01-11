import sys, re, os

ifile = sys.argv[1]
#ofile = sys.argv[2]
cpt_num = re.search("greek-boy-ch(\d+).md", ifile)[1]

ofile = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'src', ifile)


#cpt_num = f"{int(sys.argv[3]):2d}"


line_num = 0
with open(ifile, 'r', encoding="UTF-8") as i:
    with open(ofile, 'w', encoding="UTF-8") as o:
        for l in i:
            if l.strip():
                line_num += 1
                print(f"{cpt_num}.{line_num} {l.strip()}", file=o)
