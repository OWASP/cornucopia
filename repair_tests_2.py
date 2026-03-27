import os, glob, re

BASE = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org'

# 1. Fix the corrupted parenthesis in fileSystemHelper.ts
fsh_path = os.path.join(BASE, r'src\lib\filesystem\fileSystemHelper.ts')
with open(fsh_path, 'r', encoding='utf-8') as f:
    c = f.read()
# Revert the accidental named capture groups back to normal parentheses
c = re.sub(r'\(\?<g\d+>', '(', c)
with open(fsh_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

# 2. Restore missing FileSystemHelper imports where needed
for p in glob.glob(os.path.join(BASE, 'src', '**', '*.ts'), recursive=True):
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # If the file uses FileSystemHelper, isn't the helper itself, and is missing the import
    if 'FileSystemHelper' in c and 'import { FileSystemHelper }' not in c and 'export class FileSystemHelper' not in c:
        # SvelteKit uses $lib aliases, making this import path universally safe
        c = "import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';\n" + c
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(c)
        print(f"Restored import in: {p}")

print("Test repair complete! Ready to re-test.")