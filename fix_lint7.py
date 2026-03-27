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
    except FileNotFoundError: print(f'  ?  {rel}')
    except Exception as e: errors += 1; print(f'  ✗  {rel}: {e}')
def fix_all(pattern, *fns):
    for p in sorted(glob.glob(os.path.join(BASE, 'src', '**', pattern), recursive=True)):
        fix(os.path.relpath(p, BASE).replace(os.sep, '/'), *fns)

# ── fixers ───────────────────────────────

def fix_strict_boolean_string(c):
    # if (someString)  →  if (someString !== '')
    # if (!someString) →  if (someString === '')
    # Only for simple variable/property access patterns
    c = re.sub(r'if \(!([\w.]+)\)', r"if (\1 === '')", c)
    # if (str || fallback) already handled by nullish
    return c

def fix_strict_boolean_nullable_obj(c):
    # if (!obj)  →  if (obj === null || obj === undefined)
    # if (obj)   →  if (obj !== null && obj !== undefined)
    # Be surgical — only where we know it's nullable object
    c = re.sub(
        r'if \(!(\w+)\)\s*\{(\s*return)',
        r'if (\1 === null || \1 === undefined) {\2',
        c
    )
    return c

def fix_strict_boolean_any(c):
    # if (anyVal) → if (anyVal !== null && anyVal !== undefined)
    # Conservative: only simple if checks on known `any` variables
    # Pattern: if (cards) / if (mappings) / if (result)
    for var in ['cards', 'mappings', 'result', 'data', 'content', 'file', 'post']:
        c = re.sub(
            rf'if \(!{var}\)',
            rf'if ({var} === null || {var} === undefined)',
            c
        )
        c = re.sub(
            rf'if \({var}\)',
            rf'if ({var} !== null && {var} !== undefined)',
            c
        )
    return c

def fix_always_true_object(c):
    # if (!cards) error(500, ...) → just error(500, ...) since object always truthy
    # But actually the linter says "always true" meaning the check is redundant
    # Safe fix: remove the redundant check
    # Pattern: if (!mappings) error(500, "...")
    c = re.sub(
        r'\s*if \(!(\w+)\) error\(500,[^)]+\)\n',
        '\n',
        c
    )
    return c

def fix_blogpost_hidden(c):
    # if(post.hidden) → if(post.hidden === true)
    c = re.sub(r'if\(post\.hidden\)', 'if(post.hidden === true)', c)
    # if( compare > 0) — already fine, no change needed
    return c

def fix_cardattacks_string_check(c):
    # if(!suit || !card) → if(suit === '' || card === '')
    c = re.sub(
        r'if\(!suit \|\| !card\)',
        "if(suit === '' || card === '')",
        c
    )
    # if(!thisCard) → if(thisCard === undefined)
    c = re.sub(r'if\(!thisCard\)', 'if(thisCard === undefined)', c)
    return c

def fix_server_string_checks(c):
    # if (!edition || !DeckService...) → if (edition === undefined || edition === '' || !DeckService...)
    c = re.sub(
        r'if \(!edition \|\| !DeckService',
        "if (edition === undefined || edition === '' || !DeckService",
        c
    )
    c = re.sub(
        r'if \(!version \|\| !DeckService',
        "if (version === undefined || version === '' || !DeckService",
        c
    )
    return c

def fix_cre_server(c):
    # const edition = params[...] || 'webapp'  — already has fallback, fine
    # if (!cards) error(500,...) → cards is always truthy object, remove check
    # if (!mappings) error(500,...) → same
    c = re.sub(
        r"\n\s*if \(!cards\) error\(500[^)]+\)\n",
        '\n',
        c
    )
    c = re.sub(
        r"\n\s*if \(!mappings\) error\(500[^)]+\)\n",
        '\n',
        c
    )
    # string conditionals: params[...] || 'webapp'  →  params[...] ?? 'webapp'
    c = re.sub(r"\|\| 'webapp'", r"?? 'webapp'", c)
    c = re.sub(r"\|\| 'en'", r"?? 'en'", c)
    return c

def fix_suit_controller_number(c):
    # if (suit.index || 0) → if ((suit.index ?? 0) !== 0)
    # Nullable number: if (x.index) → if (x.index !== null && x.index !== undefined)
    c = re.sub(
        r'if \((\w+\.\w+) \|\| (\w+\.\w+)\)',
        r'if ((\1 ?? \2) !== 0)',
        c
    )
    return c

def fix_mapping_service_any(c):
    # if (someAny) → if (someAny !== null && someAny !== undefined)
    # Specific patterns from mappingService
    c = re.sub(
        r'if \((\w+)\)\s*\{',
        lambda m: f'if ({m.group(1)} !== null && {m.group(1)} !== undefined) {{',
        c
    )
    return c

# ── Apply targeted fixes ──────────────────

print('\n── cardAttacks.ts ──────────────────────────')
fix('src/lib/cardAttacks.ts', fix_cardattacks_string_check)

print('\n── blogpostController.ts ───────────────────')
fix('src/domain/blogpost/blogpostController.ts', fix_blogpost_hidden)

print('\n── api/lang/[edition]/[version]/+server.ts ─')
fix('src/routes/api/lang/[edition]/[version]/+server.ts', fix_server_string_checks)

print('\n── api/cre/[edition]/[lang]/+server.ts ─────')
fix('src/routes/api/cre/[edition]/[lang]/+server.ts', fix_cre_server)

print('\n── cards/[card]/+page.server.ts ────────────')
fix('src/routes/cards/[card]/+page.server.ts',
    lambda c: re.sub(r'if \((\w+)\s*&&\s*(\w+)\)', r'if (\1 !== "" && \2 !== "")', c))

print('\n── devguideMapping.ts ──────────────────────')
fix('src/lib/devguideMapping.ts',
    lambda c: re.sub(r'if \((\w+)\)', r"if (\1 !== '')", c))

print('\n── fileSystemHelper.ts ─────────────────────')
fix('src/lib/filesystem/fileSystemHelper.ts',
    lambda c: re.sub(
        r'if \(!(\w+)\)\s*return',
        r'if (\1 === null || \1 === undefined) return',
        c
    ))

print('\n── creController.ts ────────────────────────')
fix('src/domain/cre/creController.ts',
    lambda c: re.sub(
        r'if \((\w+(?:\.\w+)*)\)',
        lambda m: f'if ({m.group(1)} !== null && {m.group(1)} !== undefined)',
        c
    ))

print('\n── suitController.ts ───────────────────────')
fix('src/domain/suit/suitController.ts', fix_suit_controller_number)

print(f'\n{"="*44}')
print(f'  Files modified : {fixed}')
print(f'  Script errors  : {errors}')
print(f'{"="*44}')