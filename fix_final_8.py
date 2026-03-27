import os, re

BASE = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org'

def modify_file(rel_path, replacements):
    path = os.path.join(BASE, rel_path.replace('/', os.sep))
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    for old, new in replacements:
        if callable(new): # Handle regex replacements
            c = re.sub(old, new, c)
        else:
            c = c.replace(old, new)
    if c != orig:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(c)
        print(f"Fixed: {rel_path}")

# 1. Fix missing radix (parseInt requires base 10) in text.ts
modify_file('src/lib/utils/text.ts', [
    (r'parseInt\(parts\[0\]\)', r'parseInt(parts[0], 10)'),
    (r'parseInt\(parts\[1\]\)', r'parseInt(parts[1], 10)'),
    (r'parseInt\(parts\[2\]\)', r'parseInt(parts[2], 10)'),
])

# 2. Fix the thrown primitive errors in api server
modify_file('src/routes/api/lang/[edition]/[version]/+server.ts', [
    ('throw 404;', 'throw new Error("404");'),
    ('throw 500;', 'throw new Error("500");')
])

# 3. Fix the array iteration warning in deckService
# guard-for-in and no-for-in-array
modify_file('src/lib/services/deckService.ts', [
    ('for (const editionIndex in config.editions) {', 'for (const editionIndex of Object.keys(config.editions)) {')
])

# 4. Fix arrow-body-style in capecMapTable.test.ts (implicit return)
modify_file('src/lib/components/capecMapTable.test.ts', [
    (r'=> {\n\s*return \[', r'=> ['),
    (r'\];\n\s*\}\)', r'])')
])

print("\nFinal 8 fixes applied!")