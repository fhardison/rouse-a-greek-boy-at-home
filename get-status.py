with open("README.md", 'r') as f:
    status_table_lines = []
    progress_found = False
    sections = f.read().split('#')

    #print(sections)
    progress = None
    for s in sections:
        if " Progress\n" in s:
            progress = s.strip()
    #print(progress)
    table = progress.split("\n")[4:]
    done = []
    for line in table:
        if "| Y |" in line.upper():
            done.append(line)
    print(f"{len(done)}/{len(table)}")
