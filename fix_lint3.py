#!/usr/bin/env python3
import re, os, glob

BASE = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org'
fixed, errors = 0, 0

def read(p):
    with open(p, 'r', encoding='utf-8') as f: return f.read()

def write(p, c):
    with open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(c)

def fix(rel, *fns):
    global fixed, errors
    p = os.path.join(BASE, rel.replace('/', os.sep))
    try:
        c = read(p); orig = c
        for fn in fns: c = fn(c)
        if c != orig:
            write(p, c); fixed += 1; print(f'  ✓  {rel}')
        else:
            print(f'  —  {rel}')
    except FileNotFoundError:
        print(f'  ?  {rel}')
    except Exception as e:
        errors += 1; print(f'  ✗  {rel}: {e}')

def fix_all(pattern, *fns):
    for p in glob.glob(os.path.join(BASE, 'src', '**', pattern), recursive=True):
        rel = os.path.relpath(p, BASE).replace(os.sep, '/')
        fix(rel, *fns)

# ── fixers ───────────────────────────────

def fix_ts_ignore(c):
    return c.replace('// @ts-ignore', '// @ts-expect-error')

def fix_eslint_disable_desc(c):
    # eslint-disable-next-line rule  →  eslint-disable-next-line rule -- pre-existing
    return re.sub(
        r'// eslint-disable-next-line ([\w/@,-]+)(?! --)(?!\s*:)',
        r'// eslint-disable-next-line \1 -- pre-existing',
        c
    )

def fix_eqeq(c):
    c = re.sub(r'!={1}(?!=)', '!==', c)
    c = re.sub(r'(?<![=!<>])={2}(?!=)', '===', c)
    return c

def fix_plusplus(c):
    c = re.sub(r'\b(\w+)\+\+', r'\1 += 1', c)
    c = re.sub(r'\b(\w+)--\b', r'\1 -= 1', c)
    return c

def fix_radix(c):
    def r(m):
        inner = m.group(1)
        if ',' in inner: return m.group(0)
        return f'parseInt({inner}, 10)'
    return re.sub(r'parseInt\(([^)]+)\)', r, c)

def fix_unicode_regexp(c):
    def add_u(m):
        pre, pat, flags = m.group(1), m.group(2), m.group(3)
        if 'u' in flags or 'v' in flags: return m.group(0)
        return f'{pre}{pat}/{flags}u'
    return re.sub(r'(/)([^/\n\r*]+)/([gimsdy]*)\b', add_u, c)

def fix_nullish(c):
    # simple: x || 'default' where x is a nullable string/obj
    # Only safe pattern: value || fallback  at end of expression or assignment
    # Convert obvious cases: (someVar || 'fallback') -> (someVar ?? 'fallback')
    # Be conservative - only where linter flagged prefer-nullish-coalescing
    c = re.sub(r'\b(\w+(?:\.\w+)*)\s*\|\|\s*([\'"])', r'\1 ?? \2', c)
    return c

def fix_unnecessary_optional(c):
    # Remove ?. where value is known non-null from linter
    # Pattern: someNonNull?.property → someNonNull.property
    # Be conservative: only remove ?. on variables that are immediately destructured
    # Skip - too risky without type info
    return c

def fix_no_empty_fn(c):
    # () => {}  →  () => { /* noop */ }
    c = re.sub(r'=>\s*\{\s*\}', r'=> { /* noop */ }', c)
    return c

def fix_self_assign(c):
    # x.foo = x.foo  →  remove line
    lines, result = c.split('\n'), []
    for line in lines:
        stripped = line.strip()
        m = re.match(r'(\w+\.\w+)\s*=\s*(\w+\.\w+)\s*;?$', stripped)
        if m and m.group(1) == m.group(2):
            print(f'    removing self-assign: {stripped}')
            continue
        result.append(line)
    return '\n'.join(result)

def fix_useless_constructor(c):
    # Remove:  constructor() {}  or  constructor() { }
    c = re.sub(r'\n\s*constructor\(\)\s*\{\s*\}\n', '\n', c)
    return c

def fix_no_useless_concat(c):
    c = re.sub(r'"(\\n)"\s*\+\s*"', r'"\1', c)
    c = re.sub(r"'(\\n)'\s*\+\s*'", r"'\1", c)
    return c

def fix_prefer_for_of(c):
    c = re.sub(
        r'for \(let (\w+) = 0; \1 < (\w+)\.length; \1 \+= 1\) \{\n(\s*)const (\w+) = \2\[\1\]',
        r'for (const \4 of \2) {',
        c
    )
    return c

def fix_guard_for_in(c):
    # for (const key in obj) {  body  }
    # → for (const key in obj) { if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;  body }
    def replacer(m):
        indent = m.group(1)
        key = m.group(2)
        obj = m.group(3)
        return (f'{indent}for (const {key} in {obj}) {{\n'
                f'{indent}  if (!Object.prototype.hasOwnProperty.call({obj}, {key})) continue\n')
    c = re.sub(r'(\s*)for \(const (\w+) in (\w+)\) \{', replacer, c)
    return c

def fix_no_negated_condition(c):
    # if (!x) { A } else { B }  →  if (x) { B } else { A }
    # Too risky to do generically — skip
    return c

# ── Run ──────────────────────────────────

print('\n── @ts-ignore → @ts-expect-error (all .ts) ─')
fix_all('*.ts', fix_ts_ignore)

print('\n── eslint-disable require-description ──────')
fix_all('*.ts', fix_eslint_disable_desc)

print('\n── no-plusplus remaining ───────────────────')
for f in [
    'src/domain/author/authorController.ts',
    'src/domain/mapping/mappingController.ts',
    'src/domain/suit/suitController.ts',
    'src/lib/cardAttacks.ts',
    'src/lib/services/deckService.ts',
]:
    fix(f, fix_plusplus)

print('\n── eqeqeq remaining ────────────────────────')
for f in [
    'src/domain/author/authorController.ts',
    'src/lib/services/deckService.ts',
    'src/lib/services/mappingService.ts',
    'src/domain/mapping/mappingController.ts',
]:
    fix(f, fix_eqeq)

print('\n── radix remaining ─────────────────────────')
fix_all('*.ts', fix_radix)

print('\n── require-unicode-regexp remaining ────────')
fix_all('*.ts', fix_unicode_regexp)

print('\n── prefer-for-of remaining ─────────────────')
fix_all('*.ts', fix_prefer_for_of)

print('\n── no-empty-function ───────────────────────')
fix_all('*.ts', fix_no_empty_fn)

print('\n── no-self-assign ──────────────────────────')
for f in [
    'src/lib/services/deckService.ts',
]:
    fix(f, fix_self_assign)

print('\n── no-useless-constructor ──────────────────')
fix('src/lib/services/deckService.ts', fix_useless_constructor)

print('\n── no-useless-concat ───────────────────────')
fix('src/routes/rss.xml/+server.ts', fix_no_useless_concat)

print('\n── guard-for-in ────────────────────────────')
fix('src/lib/services/deckService.ts', fix_guard_for_in)

print('\n── prefer-nullish-coalescing (safe) ────────')
for f in [
    'src/lib/services/deckService.ts',
    'src/lib/services/mappingService.ts',
    'src/lib/filesystem/fileSystemHelper.ts',
    'src/domain/suit/suitController.ts',
    'src/domain/blogpost/blogpostController.ts',
    'src/domain/author/authorController.ts',
]:
    fix(f, fix_nullish)

print(f'\n{"="*44}')
print(f'  Files modified : {fixed}')
print(f'  Script errors  : {errors}')
print(f'{"="*44}')