import re, os

BASE = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org'
fixed = 0

def read(rel):
    with open(os.path.join(BASE, rel.replace('/', os.sep)), 'r', encoding='utf-8') as f: return f.read()
def write(rel, c):
    with open(os.path.join(BASE, rel.replace('/', os.sep)), 'w', encoding='utf-8', newline='\n') as f: f.write(c)
def fix(rel, fn):
    global fixed
    try:
        orig = read(rel); c = fn(orig)
        if c != orig: write(rel, c); fixed += 1; print(f'  fixed: {rel}')
        else: print(f'  no change: {rel}')
    except Exception as e: print(f'  error: {rel}: {e}')

def fix_cre_controller(c):
    c = c.replace('(this.deck || []).forEach', 'this.deck.forEach')
    c = re.sub(r'const cre = [^\n]+\n\s*if \(!cre\) \{\n\s*throw Error[^\n]+\n\s*\}\n', 'const cre = (mapping.owasp_cre?.owasp_asvs as string[]) ?? []\n', c)
    c = c.replace('return CreController.editions.get(edition) || edition', 'return CreController.editions.get(edition) ?? edition')
    return c

def fix_mapping_service(c):
    c = c.replace("mapping?.version === 'latests'", "mapping !== null && mapping !== undefined && (mapping as any).version === 'latests'")
    c = c.replace("mapping?.edition === edition", "(mapping as any).edition === edition")
    c = c.replace("mapping?.version === deck.version", "(mapping as any).version === deck.version")
    c = c.replace("mapping?.edition === deck.edition", "(mapping as any).edition === deck.edition")
    c = c.replace('if (!mappingData) {', 'if (mappingData === null || mappingData === undefined) {')
    c = c.replace('if (mappingData) {', 'if (mappingData !== null && mappingData !== undefined) {')
    return c

def fix_author_controller(c):
    c = c.replace('return getAuthors().find((x) => x.name === name) || ({} as Author)', 'return getAuthors().find((x) => x.name === name) ?? ({} as Author)')
    return c

def fix_suit_controller(c):
    c = re.sub(r'(\w+\.\w+) \|\| 0\b', r'\1 ?? 0', c)
    return c

def fix_filesystem_helper(c):
    c = re.sub(r'if \((\w+) &&', r'if (\1 !== null && \1 !== undefined &&', c)
    return c

fix('src/domain/cre/creController.ts', fix_cre_controller)
fix('src/lib/services/mappingService.ts', fix_mapping_service)
fix('src/domain/author/authorController.ts', fix_author_controller)
fix('src/domain/suit/suitController.ts', fix_suit_controller)
fix('src/lib/filesystem/fileSystemHelper.ts', fix_filesystem_helper)

print(f'\nTotal modified: {fixed}')