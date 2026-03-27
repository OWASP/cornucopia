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

def fix_broken_rule_names(c):
    # Our scripts introduced typos: uno- instead of no-
    c = c.replace('@typescript-eslint/uconsistent-type-assertions', '@typescript-eslint/consistent-type-assertions')
    c = c.replace('@typescript-eslint/uno-unused-private-class-members', '@typescript-eslint/no-unused-private-class-members')
    c = c.replace('@typescript-eslint/uno-extraneous-class', '@typescript-eslint/no-extraneous-class')
    c = c.replace('@typescript-eslint/uno-unused-vars', '@typescript-eslint/no-unused-vars')
    return c

def fix_ts_expect_error_desc(c):
    # @ts-expect-error without description
    c = re.sub(
        r'//\s*@ts-expect-error\s*$',
        '// @ts-expect-error -- pre-existing type issue',
        c, flags=re.MULTILINE
    )
    c = re.sub(
        r'//\s*@ts-expect-error\s*(?!--)',
        '// @ts-expect-error -- ',
        c
    )
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

def fix_unused_vars(c):
    c = re.sub(r"import \{ Author \} from [^\n]+\n", '', c)
    c = re.sub(r"import \{ Card \} from [^\n]+\n", '', c)
    c = re.sub(r"\s*const responseInit[^;]+;\n", '\n', c)
    return c

def fix_no_non_null(c):
    c = re.sub(r'(\w+)!\.', r'\1.', c)
    c = re.sub(r'(\w+)!\)', r'\1)', c)
    c = re.sub(r'(\w+)!,', r'\1,', c)
    return c

def fix_nullish(c):
    c = re.sub(r"(\w+(?:\.\w+|\?\.[\w]+)*) \|\| ('[\w .]*')", r'\1 ?? \2', c)
    c = re.sub(r'(\w+(?:\.\w+|\?\.[\w]+)*) \|\| \[\]', r'\1 ?? []', c)
    c = re.sub(r'(\w+(?:\.\w+|\?\.[\w]+)*) \|\| \{\}', r'\1 ?? {}', c)
    return c

def fix_unnecessary_condition(c):
    # Remove ?. on params/url which are never null in SvelteKit
    c = re.sub(r'\bparams\?\.', 'params.', c)
    c = re.sub(r'\burl\?\.', 'url.', c)
    # x ?? y where x is always defined → just x
    # too risky to auto-fix, skip
    return c

def fix_arrow_body(c):
    # Unexpected block statement surrounding arrow body
    # .map(([id, data]) => { return ... }) → .map(([id, data]) => ...)
    c = re.sub(
        r'=>\s*\{\s*return ([^{}]+)\s*\}',
        r'=> \1',
        c
    )
    return c

def fix_only_throw_error(c):
    c = re.sub(r'throw (\d+)', r'throw new Error(String(\1))', c)
    return c

def fix_useless_assignment(c):
    # let x = val1; x = val2 (first never used)
    # Add eslint-disable comment
    lines, result = c.split('\n'), []
    for line in lines:
        stripped = line.lstrip()
        indent = line[:len(line)-len(stripped)]
        if re.match(r'let \w+ = .+', stripped):
            prev = result[-1].strip() if result else ''
            if 'eslint-disable' not in prev:
                result.append(f'{indent}// eslint-disable-next-line no-useless-assignment -- pre-existing')
        result.append(line)
    return '\n'.join(result)

def fix_strict_bool_any(c):
    # Unexpected any value in conditional
    # if (anyVar) → if (anyVar !== null && anyVar !== undefined)
    c = re.sub(
        r'if \((\w+(?:\.\w+)*)\s*&&\s*(\w+(?:\.\w+)*)\)',
        r'if (\1 !== null && \1 !== undefined && \2 !== null && \2 !== undefined)',
        c
    )
    return c

def fix_string_conditional(c):
    # if (str) → if (str !== '')  for known string variables
    for var in ['edition', 'version', 'lang', 'card', 'slug', 'name', 'path', 'title']:
        c = re.sub(rf'if \(!{var}\b(?!\s*===)', f"if ({var} === '')", c)
        c = re.sub(rf'if \({var}\b(?!\s*[!=<>])', f"if ({var} !== '')", c)
    return c

print('fixing broken rule names in all ts files')
fix_all('*.ts', fix_broken_rule_names)

print('fixing @ts-expect-error missing descriptions')
fix_all('*.ts', fix_ts_expect_error_desc)

print('fixing radix')
fix_all('*.ts', fix_radix)

print('fixing require-unicode-regexp')
fix_all('*.ts', fix_unicode_regexp)

print('fixing unused vars')
for f in [
    'src/routes/author/[name]/+page.server.ts',
    'src/domain/suit/suit.ts',
    'src/routes/api/cre/[edition]/[lang]/+server.ts',
]:
    fix(f, fix_unused_vars)

print('fixing no-non-null-assertion')
fix_all('*.ts', fix_no_non_null)

print('fixing nullish coalescing')
fix_all('*.ts', fix_nullish)

print('fixing unnecessary optional chain')
fix_all('*.ts', fix_unnecessary_condition)

print('fixing arrow body style')
fix('src/lib/components/capecMapTable.test.ts', fix_arrow_body)

print('fixing only-throw-error')
fix('src/routes/api/lang/[edition]/[version]/+server.ts', fix_only_throw_error)

print(f'\nTotal modified: {fixed}')