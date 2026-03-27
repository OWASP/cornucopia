import os, glob
base = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org\src'
for p in glob.glob(base + r'\**\*.ts', recursive=True):
    c = open(p, encoding='utf-8').read()
    c2 = (c
        .replace('uno-unused-private-class-members', 'no-unused-private-class-members')
        .replace('uno-extraneous-class', 'no-extraneous-class')
        .replace('uconsistent-type-assertions', 'consistent-type-assertions')
    )
    if c != c2:
        open(p, 'w', encoding='utf-8', newline='\n').write(c2)
        print('fixed:', os.path.relpath(p, base))