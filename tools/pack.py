"""Sync src/template.html with the __bundler/template block inside index.html.

The site is a single self-contained index.html (an exported artifact bundle).
The actual app markup + logic lives as a JSON-encoded string in a
<script type="__bundler/template"> block. Edit src/template.html, then run:

    python tools/pack.py          # src/template.html -> index.html
    python tools/pack.py unpack   # index.html -> src/template.html

Fonts and the runtime live in the __bundler/manifest block and never need
touching.
"""
import json
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SRC = ROOT / "src" / "template.html"

BLOCK = re.compile(r'(<script type="__bundler/template">\s*)(.*?)(\s*</script>)', re.S)


def find_block(html):
    m = BLOCK.search(html)
    if not m:
        sys.exit("no __bundler/template block found in index.html")
    return m


def pack():
    html = INDEX.read_text(encoding="utf-8")
    m = find_block(html)
    tpl = SRC.read_text(encoding="utf-8").replace("\r\n", "\n")
    # Escape "</" so the JSON string can't terminate the <script> block.
    enc = json.dumps(tpl, ensure_ascii=False).replace("</", "<\\/")
    out = html[: m.start(2)] + enc + html[m.end(2):]
    with open(INDEX, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"packed {SRC.name} -> index.html ({len(enc):,} chars)")


def unpack():
    html = INDEX.read_text(encoding="utf-8")
    m = find_block(html)
    SRC.parent.mkdir(exist_ok=True)
    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(json.loads(m.group(2)))
    print(f"unpacked index.html -> {SRC.relative_to(ROOT)}")


if __name__ == "__main__":
    (unpack if "unpack" in sys.argv[1:] else pack)()
