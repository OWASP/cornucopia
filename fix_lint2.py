#!/usr/bin/env python3
import re, os

BASE = r'C:\Users\KIIT\cornucopia\cornucopia.owasp.org'
fixed, errors = 0, 0

def read(rel):
    with open(os.path.join(BASE, rel.replace('/', os.sep)), 'r', encoding='utf-8') as f:
        return f.read()

def write(rel, content):
    with open(os.path.join(BASE, rel.replace('/', os.sep)), 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def fix(rel, *fns):
    global fixed, errors
    try:
        c = read(rel)
        orig = c
        for fn in fns: c = fn(c)
        if c != orig:
            write(rel, c)
            fixed += 1
            print(f'  ✓  {rel}')
        else:
            print(f'  —  {rel}')
    except FileNotFoundError:
        print(f'  ?  {rel} (not found)')
    except Exception as e:
        errors += 1
        print(f'  ✗  {rel}: {e}')

# ── Fix functions ─────────────────────────

def fix_ts_ignore(c):
    return c.replace('// @ts-ignore', '// @ts-expect-error')

def fix_eqeq(c):
    # Fix != before == to avoid double replacement issues
    c = re.sub(r'!={1}(?!=)', '!==', c)
    c = re.sub(r'(?<![=!<>])={2}(?!=)', '===', c)
    return c

def fix_plusplus(c):
    c = re.sub(r'\b(\w+)\+\+', r'\1 += 1', c)
    c = re.sub(r'\b(\w+)--\b', r'\1 -= 1', c)
    return c

def fix_no_console(c):
    lines, result = c.split('\n'), []
    for line in lines:
        stripped = line.lstrip()
        if re.match(r'console\.(log|error|warn|info|debug)\s*\(', stripped):
            prev = result[-1].strip() if result else ''
            if 'eslint-disable' not in prev:
                indent = ' ' * (len(line) - len(stripped))
                result.append(f'{indent}// eslint-disable-next-line no-console')
        result.append(line)
    return '\n'.join(result)

def fix_radix(c):
    # Only add radix if not already there
    def replacer(m):
        inner = m.group(1)
        if ',' in inner:
            return m.group(0)  # already has radix
        return f'parseInt({inner}, 10)'
    return re.sub(r'parseInt\(([^)]+)\)', replacer, c)

def rm_async_arrow(c):
    # async () => with no await inside: remove async keyword
    # Only for simple test callbacks like: async () => {
    lines = c.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Match: async () => { or async ({ ... }) => {
        if re.search(r'\basync\s+(\(\)|(\([^)]+\)))\s*=>\s*\{', line):
            # Check if next ~20 lines contain await
            block = '\n'.join(lines[i:i+25])
            if 'await ' not in block:
                line = re.sub(r'\basync\s+(\()', r'\1', line)
        result.append(line)
        i += 1
    return '\n'.join(result)

def rm_unused_import(name):
    def fn(c):
        c = re.sub(rf"import \{{ {name} \}} from [^\n]+\n", '', c)
        c = re.sub(rf",\s*{name}\b", '', c)
        c = re.sub(rf"\b{name}\s*,\s*", '', c)
        return c
    return fn

def rm_var(name):
    return lambda c: re.sub(rf'\s*(?:const|let|var) {name}\s*=[^\n]+\n', '\n', c)

def fix_prefer_for_of(c):
    # for (let i = 0; i < arr.length; i += 1) { const x = arr[i]
    c = re.sub(
        r'for \(let (\w+) = 0; \1 < (\w+)\.length; \1 \+= 1\) \{\n(\s*)const (\w+) = \2\[\1\]',
        r'for (const \4 of \2) {',
        c
    )
    return c

def fix_no_useless_concat(c):
    c = re.sub(r'"\\n"\s*\+\s*"', '"\\n', c)
    c = re.sub(r"'\\n'\s*\+\s*'", "'\\n", c)
    return c

def fix_no_tostring(c):
    return re.sub(r'(\w+)\.toString\(\)', r'\1', c)

def fix_ban_ts_comment(c):
    return c.replace('// @ts-ignore', '// @ts-expect-error')

def fix_async_load(c):
    return c.replace('export async function load', 'export function load')

# ── Apply ─────────────────────────────────

print('\n── authorController (correct path) ────────')
fix('src/domain/author/authorController.ts', fix_eqeq, fix_plusplus)

print('\n── blogpostController ──────────────────────')
fix('src/domain/blogpost/blogpostController.ts', fix_ban_ts_comment, fix_eqeq, fix_no_console)

print('\n── mappingController ───────────────────────')
fix('src/domain/mapping/mappingController.ts', fix_eqeq, fix_plusplus)

print('\n── suitController ──────────────────────────')
fix('src/domain/suit/suitController.ts', fix_plusplus)

print('\n── cardAttacks ─────────────────────────────')
fix('src/lib/cardAttacks.ts', fix_eqeq, fix_plusplus)

print('\n── deckService ─────────────────────────────')
fix('src/lib/services/deckService.ts', fix_eqeq, fix_no_console, fix_plusplus)

print('\n── mappingService ──────────────────────────')
fix('src/lib/services/mappingService.ts', fix_eqeqeq := fix_eqeq, fix_no_console)

print('\n── capecService ────────────────────────────')
fix('src/lib/services/capecService.ts', fix_no_console)

print('\n── fileSystemHelper ────────────────────────')
fix('src/lib/filesystem/fileSystemHelper.ts', fix_eqeq)

print('\n── rss.xml server ──────────────────────────')
fix('src/routes/rss.xml/+server.ts',
    fix_no_useless_concat, fix_prefer_for_of, fix_plusplus, fix_radix, fix_no_tostring)

print('\n── text.ts ─────────────────────────────────')
fix('src/lib/utils/text.ts', fix_radix, fix_plusplus)

print('\n── unused vars ─────────────────────────────')
fix('src/routes/author/[name]/+page.server.ts', rm_unused_import('Author'))
fix('src/routes/api/cre/[edition]/[lang]/+server.ts', rm_var('responseInit'))
fix('src/domain/suit/suit.ts', rm_unused_import('Card'))

print('\n── require-await in test files ─────────────')
for f in [
    'src/lib/devGuideMapping.test.ts',
    'src/lib/filesystem/fileSystemHelper.test.ts',
    'src/lib/services/mappingService.test.ts',
    'src/lib/services/decService.integration.test.ts',
    'src/domain/mapping/mappingController.test.ts',
    'src/domain/mapping/mastg.test.ts',
]:
    fix(f, rm_async_arrow)

print('\n── copi/+page.server.ts ────────────────────')
fix('src/routes/copi/+page.server.ts', fix_async_load)

print(f'\n{"="*44}')
print(f'  Files modified : {fixed}')
print(f'  Script errors  : {errors}')
print(f'{"="*44}')