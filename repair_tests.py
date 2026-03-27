import os, glob

BASE = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org'

def repair_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    
    # 1. Fix the corrupted file paths (remove the chained 'u's)
    content = content.replace('uuuuuu', '')
    content = content.replace('uuuuu', '')
    content = content.replace('uuuu', '')
    
    # 2. Fix the duplicate 'u' flag in the regex in devguideMapping.ts
    content = content.replace('/[0-9-]+/ugu', '/[0-9-]+/gu')

    # 3. Restore the missing FileSystemHelper import in the test file
    if 'fileSystemHelper.test.ts' in path.replace('\\', '/'):
        if 'import { FileSystemHelper }' not in content:
            content = "import { FileSystemHelper } from './fileSystemHelper';\n" + content

    if content != orig:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"Repaired: {path}")

for p in glob.glob(os.path.join(BASE, 'src', '**', '*.ts'), recursive=True):
    repair_file(p)

print("Repair complete!")