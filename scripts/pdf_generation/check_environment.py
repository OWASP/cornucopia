"""
Report which Python interpreter is being used and whether the packages the
generator needs are importable.

Scribus runs scripts in its own interpreter, which is often not the `python3`
on your PATH. When package installation appears to have worked but the
generator still reports a missing module, this shows where the interpreter is
actually looking.

Run it both ways and compare:

    python3 check_environment.py

    /Applications/Scribus.app/Contents/MacOS/Scribus --no-splash --no-gui \
      --python-script check_environment.py          (macOS)

    "C:\\Program Files\\Scribus 1.6.6\\Scribus.exe" --no-splash --no-gui ^
      --python-script check_environment.py          (Windows)

    scribus --no-splash --no-gui --python-script check_environment.py  (Linux)

Inside Scribus the output also goes to check_environment.txt next to this
script, because Scribus does not always show console output.
"""

import os
import sys

# name -> (package to install, needed in Scribus?, needed in system Python?)
REQUIRED = {
    'yaml': ('pyyaml', True, True),
    'qrcode': ('qrcode', True, False),
    'png': ('pypng, so qrcode works without Pillow', True, False),
    'pymupdf': ('pymupdf, for merge_pdfs.py', False, True),
}


def report():
    lines = []
    add = lines.append

    try:
        import scribus  # noqa: F401
        in_scribus = True
        add("Running inside: Scribus")
    except ImportError:
        in_scribus = False
        add("Running inside: plain Python (not Scribus)")

    add("")
    add("Python version : %s" % sys.version.split()[0])
    add("Interpreter    : %s" % (sys.executable or "(embedded, no executable)"))
    add("Install prefix : %s" % sys.prefix)
    add("")
    add("Where this interpreter looks for packages:")
    for entry in sys.path:
        add("  %s" % (entry or "(current directory)"))

    add("")
    add("Packages this interpreter needs:")
    missing = []
    for name, (package, for_scribus, for_system) in REQUIRED.items():
        wanted = for_scribus if in_scribus else for_system
        try:
            module = __import__(name)
            where = getattr(module, '__file__', '(built in)')
            add("  found       %-9s %s" % (name, where))
        except ImportError:
            if wanted:
                add("  MISSING     %-9s install %s" % (name, package))
                missing.append(name)
            else:
                add("  not needed  %-9s (only used by the other interpreter)" % name)

    add("")
    if missing:
        add("Missing: %s" % ", ".join(missing))
        add("")
        add("These must be installed into THIS interpreter, not a different one.")
        add("The 'Install prefix' above identifies which Python that is. If you")
        add("installed them with a 'python3' that reports a different prefix,")
        add("they went somewhere this interpreter cannot see. See the")
        add("'Install the Python packages' section of README.md.")
    else:
        add("All packages this interpreter needs are present.")

    return "\n".join(lines)


if __name__ == "__main__":
    text = report()
    print(text)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "check_environment.txt")
    try:
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        print("\nAlso written to %s" % out)
    except Exception as exc:
        print("\nCould not write report file: %s" % exc)
