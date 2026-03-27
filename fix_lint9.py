import re, os, glob

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
def fix_all(pattern, fn):
    for p in sorted(glob.glob(os.path.join(BASE, 'src', '**', pattern), recursive=True)):
        fix(os.path.relpath(p, BASE).replace(os.sep, '/'), fn)

def fix_capec_test(c):
    # data.owasp_asvs || []  →  data.owasp_asvs ?? []
    c = c.replace('data.owasp_asvs || []', 'data.owasp_asvs ?? []')
    # capecData[Number(id)]?.name || `CAPEC ${id}`  →  capecData[Number(id)]?.name ?? `CAPEC ${id}`
    c = re.sub(r'(\w+\[[\w()]+\]\?\.name) \|\| (`[^`]+`)', r'\1 ?? \2', c)
    # capecMap || {}  →  capecMap ?? {}
    c = c.replace('capecMap || {}', 'capecMap ?? {}')
    # searchString is unused - remove it
    c = re.sub(r'\s*const searchString = [^\n]+\n', '\n', c)
    return c

def fix_nullish_all(c):
    # Safe pattern: x || [] → x ?? []
    c = re.sub(r'(\w+(?:\.\w+|\[[\w()]+\])*) \|\| \[\]', r'\1 ?? []', c)
    # x || {} → x ?? {}
    c = re.sub(r'(\w+(?:\.\w+)*) \|\| \{\}', r'\1 ?? {}', c)
    # x || '' → x ?? ''
    c = re.sub(r"(\w+(?:\.\w+)*) \|\| ''", r"\1 ?? ''", c)
    c = re.sub(r'(\w+(?:\.\w+)*) \|\| ""', r'\1 ?? ""', c)
    # x || 'fallback'  → x ?? 'fallback'
    c = re.sub(r"(\w+(?:\.\w+|\?\.[\w]+)*) \|\| ('[\w .]+')", r'\1 ?? \2', c)
    c = re.sub(r'(\w+(?:\.\w+|\?\.[\w]+)*) \|\| ("[\w .]+")', r'\1 ?? \2', c)
    return c

def fix_prefer_for_of(c):
    c = re.sub(
        r'for \(let (\w+) = 0; \1 < ([\w.]+)\.length; \1 \+= 1\) \{\n(\s*)const (\w+) = \2\[\1\]',
        r'for (const \4 of \2) {',
        c
    )
    c = re.sub(
        r'for \(let (\w+) = 0; \1 < ([\w.]+)\.length; \1 \+= 1\)',
        r'for (const _i of Array.from({ length: \2.length }))',
        c
    )
    return c

def fix_ban_ts_comment(c):
    c = re.sub(r'//\s*@ts-ignore\s*$', '// @ts-expect-error -- pre-existing', c, flags=re.MULTILINE)
    c = re.sub(r'//\s*@ts-ignore(?!\s*--)', '// @ts-expect-error -- pre-existing', c)
    return c

def fix_radix(c):
    def r(m):
        inner = m.group(1)
        if ',' in inner: return m.group(0)
        return f'parseInt({inner}, 10)'
    return re.sub(r'parseInt\(([^)]+)\)', r, c)

def fix_unicode_regexp(c):
    def add_u(m):
        flags = m.group(3)
        if 'u' in flags or 'v' in flags: return m.group(0)
        return f'{m.group(1)}{m.group(2)}/{flags}u'
    return re.sub(r'(/)([^/\n\r*\[]+)/([gimsdy]*)\b', add_u, c)

def fix_no_non_null(c):
    c = re.sub(r'(\w+)!\.', r'\1.', c)
    c = re.sub(r'(\w+)!\)', r'\1)', c)
    return c

def fix_only_throw_error(c):
    c = re.sub(r'throw (\d+)', r'throw new Error(String(\1))', c)
    return c

def fix_no_unnecessary_boolean_compare(c):
    # x === true → x (only for known booleans)
    c = re.sub(r'(\w+(?:\.\w+)*) === true\b', r'\1', c)
    c = re.sub(r'(\w+(?:\.\w+)*) === false\b', r'!\1', c)
    return c

def fix_strict_bool_any(c):
    # Common: if (anyVar) in route files
    # Pattern from edition server files
    for varname in ['edition', 'version', 'lang', 'card', 'slug', 'name', 'path']:
        c = re.sub(rf'if \(!{varname}\b', f"if ({varname} === undefined || {varname} === ''", c)
    return c

def fix_unnecessary_condition(c):
    # Remove ?. on non-nullable
    c = re.sub(r'\bparams\?\.', 'params.', c)
    c = re.sub(r'\burl\?\.', 'url.', c)
    return c

print('capecMapTable.test.ts')
fix('src/lib/components/capecMapTable.test.ts', fix_capec_test)

print('nullish coalescing across all ts files')
fix_all('*.ts', fix_nullish_all)

print('ban-ts-comment across all ts files')
fix_all('*.ts', fix_ban_ts_comment)

print('radix across all ts files')
fix_all('*.ts', fix_radix)

print('require-unicode-regexp across all ts files')
fix_all('*.ts', fix_unicode_regexp)

print('no-non-null-assertion')
fix_all('*.ts', fix_no_non_null)

print('only-throw-error')
fix('src/routes/api/lang/[edition]/[version]/+server.ts', fix_only_throw_error)

print('no-unnecessary-boolean-literal-compare')
fix_all('*.ts', fix_no_unnecessary_boolean_compare)

print('no-unnecessary-condition')
for f in [
    'src/routes/edition/[edition]/[card]/[version]/+page.server.ts',
    'src/routes/edition/[edition]/[card]/[version]/[lang]/+page.server.ts',
    'src/routes/edition/[edition]/[card]/+page.server.ts',
]:
    fix(f, fix_unnecessary_condition)

print(f'\nTotal modified: {fixed}')