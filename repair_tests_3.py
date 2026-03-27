import os

BASE = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org'

# 1. Fix the '\uen\' typo in fileSystemHelper.ts
fsh = os.path.join(BASE, r'src\lib\filesystem\fileSystemHelper.ts')
with open(fsh, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('/uen/', '/en/')
c = c.replace('/uen', '/en')
with open(fsh, 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

# 2. Fix the dangerous boolean checks in deckService.ts
ds = os.path.join(BASE, r'src\lib\services\deckService.ts')
with open(ds, 'r', encoding='utf-8') as f:
    c = f.read()
# Revert the strict string checks back to standard truthy checks so undefined behaves correctly
c = c.replace("if (edition !== '')", "if (edition)")
c = c.replace("if (version !== '')", "if (version)")
c = c.replace("if (lang !== '')", "if (lang)")
with open(ds, 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print("Logic repaired! Ready for final test.")