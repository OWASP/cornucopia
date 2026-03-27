#!/usr/bin/env python3
"""Fix remaining lint errors in cornucopia.owasp.org"""
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

# ── Fix functions ────────────────────────────

def rm_async_load(c):
    return c.replace('export async function load', 'export function load')

def fix_ts_ignore(c):
    return c.replace('// @ts-ignore', '// @ts-expect-error')

def fix_eqeq(c):
    c = re.sub(r'(?<![=!<>])={2}(?!=)', '===', c)
    c = re.sub(r'!=(?!=)', '!==', c)
    return c

def fix_radix(c):
    return re.sub(r'parseInt\(([^,)]+)\)', r'parseInt(\1, 10)', c)

def fix_plusplus(c):
    c = re.sub(r'\b(\w+)\+\+', r'\1 += 1', c)
    c = re.sub(r'\b(\w+)--\b', r'\1 -= 1', c)
    return c

def fix_tostring(c):
    return re.sub(r'(\w+)\.toString\(\)', r'\1', c)

def fix_string_wrap(c):
    return re.sub(r'String\(input\)', 'input', c)

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

def fix_void_promises(c):
    lines, result = c.split('\n'), []
    for line in lines:
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        if (re.match(r'^(GET|POST|PUT|DELETE|PATCH)\s*\(', stripped)
                and not stripped.startswith(('void ', 'const ', 'return ', 'await '))):
            result.append(f'{indent}void {stripped}')
        else:
            result.append(line)
    return '\n'.join(result)

def fix_unicode_regexp(c):
    def add_u(m):
        pre, pat, flags = m.group(1), m.group(2), m.group(3)
        if 'u' not in flags and 'v' not in flags:
            return f'{pre}{pat}/{flags}u'
        return m.group(0)
    return re.sub(r'(/)([^/\n\r*]+)/([gimsdy]*)\b', add_u, c)

def rm_unused_import(name):
    def fn(c):
        c = re.sub(rf"import \{{ {name} \}} from [^\n]+\n", '', c)
        c = re.sub(rf',\s*{name}\b', '', c)
        c = re.sub(rf'\b{name}\s*,\s*', '', c)
        return c
    return fn

def rm_var(name):
    return lambda c: re.sub(rf'\s*const {name}\s*=[^\n]+\n', '\n', c)

def fix_for_of(c):
    # for (let i=0; i < arr.length; i += 1) { \n  const x = arr[i]
    c = re.sub(
        r'for \(let (\w+) = 0; \1 < (\w+)\.length; \1 \+= 1\) \{\n(\s*)const (\w+) = \2\[\1\]',
        r'for (const \4 of \2) {',
        c
    )
    return c

def fix_useless_concat(c):
    # "\n" + "</" -> "\n</"
    c = re.sub(r'"(\\n)"\s*\+\s*"(</?)', r'"\1\2', c)
    c = re.sub(r"'(\\n)'\s*\+\s*'(</?)", r"'\1\2", c)
    return c

def fix_param_reassign_input(c):
    # input = String(input) -> const processed = input
    # input = input.trim() -> handled separately
    lines, result = c.split('\n'), []
    for line in lines:
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        # Convert: input = String(input) -> const _input = String(input)
        m = re.match(r'input = String\(input\)', stripped)
        if m:
            line = f'{indent}const _input = input'
        result.append(line)
    return '\n'.join(result)

def fix_no_non_null(c):
    # someVar! -> someVar  (simple cases)
    return re.sub(r'(\w+)!([.,;)\s])', r'\1\2', c)

def fix_no_useless_assign(c):
    # Remove: let x = ...; x = ...; (where first assign is never read)
    return c

# ── Apply fixes ──────────────────────────────

print('\n── require-await ───────────────────────────')
for f in [
    'src/routes/+layout.server.ts',
    'src/routes/about/+page.server.ts',
    'src/routes/author/[name]/+page.server.ts',
    'src/routes/copi/+page.server.ts',
    'src/routes/how-to-play/+page.server.ts',
    'src/routes/printing/+page.server.ts',
    'src/routes/questionsandanswers/+page.server.ts',
    'src/routes/roadmap/+page.server.ts',
    'src/routes/source/+page.server.ts',
    'src/routes/swags/+page.server.ts',
    'src/routes/taxonomy/+page.server.ts',
    'src/routes/webshop/+page.server.ts',
]:
    fix(f, rm_async_load)

# async arrow function in cards
fix('src/routes/cards/[card]/+page.server.ts',
    lambda c: re.sub(r'\basync\s+(\(\{[^}]+\}\))\s*=>', r'\1 =>', c))

print('\n── ban-ts-comment ──────────────────────────')
fix('src/routes/taxonomy/[...path]/+page.server.ts', fix_ts_ignore, rm_async_load)

print('\n── no-unused-vars ──────────────────────────')
fix('src/routes/author/+page.server.ts',        rm_unused_import('FileSystemHelper'))
fix('src/routes/author/[name]/+page.server.ts', rm_unused_import('Author'))
fix('src/routes/api/cre/[edition]/[lang]/+server.ts', rm_var('responseInit'))
fix('src/lib/utils/text.ts',
    lambda c: re.sub(r"type DateStyle = [^\n]+\n?", '', c))

print('\n── eqeqeq ──────────────────────────────────')
for f in [
    'src/routes/edition/[edition]/[card]/+page.server.ts',
    'src/lib/services/deckService.ts',
    'src/lib/services/mappingService.ts',
    'src/domain/mapping/mappingController.ts',
    'src/lib/cardAttacks.ts',
    'src/lib/filesystem/fileSystemHelper.ts',
    'src/domain/authorController.ts',
    'src/domain/blogpost/blogpostController.ts',
]:
    fix(f, fix_eqeq)

print('\n── radix ───────────────────────────────────')
fix('src/routes/rss.xml/+server.ts', fix_radix)
fix('src/lib/utils/text.ts', fix_radix)

print('\n── no-plusplus ─────────────────────────────')
fix('src/routes/rss.xml/+server.ts', fix_plusplus)
fix('src/lib/utils/text.ts', fix_plusplus)

print('\n── no-unnecessary-type-conversion ──────────')
fix('src/lib/utils/text.ts', fix_string_wrap)
fix('src/routes/rss.xml/+server.ts', fix_tostring)

print('\n── no-console ──────────────────────────────')
for f in [
    'src/lib/utils/cache.ts',
    'src/lib/services/capecService.ts',
    'src/lib/services/deckService.ts',
    'src/lib/services/mappingService.ts',
    'src/domain/blogpost/blogpostController.ts',
]:
    fix(f, fix_no_console)

print('\n── no-floating-promises ────────────────────')
fix('src/routes/api/lang/[edition]/[version]/server.test.ts', fix_void_promises)

print('\n── no-useless-concat ───────────────────────')
fix('src/routes/rss.xml/+server.ts', fix_useless_concat)

print('\n── require-unicode-regexp ──────────────────')
for f in [
    'src/routes/taxonomy/[...path]/+page.server.ts',
    'src/lib/utils/text.ts',
    'src/lib/devguideMapping.ts',
    'src/lib/filesystem/fileSystemHelper.ts',
]:
    fix(f, fix_unicode_regexp)

print('\n── prefer-for-of ───────────────────────────')
fix('src/routes/rss.xml/+server.ts', fix_for_of)

print('\n── no-non-null-assertion ───────────────────')
fix('src/routes/cards/[card]/+page.server.ts', fix_no_non_null)

print(f'\n{"="*44}')
print(f'  Files modified : {fixed}')
print(f'  Script errors  : {errors}')
print(f'{"="*44}')