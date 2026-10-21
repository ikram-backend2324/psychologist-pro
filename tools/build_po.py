"""Collect UI strings from templates/Python and write locale/<lang>/LC_MESSAGES/django.po.

Translations live in tools/translations.py as {msgid: (uz, kaa, ru)}. Usage:
    python tools/build_po.py            # write .po files, report missing strings
    python tools/build_po.py --list     # print every msgid found
Then run `python manage.py compile_translations`.
"""
import ast
import re
import sys
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from translations import EXTRA, PLURAL, TRANSLATIONS  # noqa: E402

LANGS = ("uz", "kaa", "ru")
PLURALS = {"uz": "nplurals=1; plural=0;", "kaa": "nplurals=1; plural=0;", "ru": "nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);"}

TEMPLATE_PATTERNS = [
    re.compile(r"""{%\s*translate\s+"((?:[^"\\]|\\.)*)"\s*(?:as \w+\s*)?%}"""),
    re.compile(r"""{%\s*translate\s+'((?:[^'\\]|\\.)*)'\s*(?:as \w+\s*)?%}"""),
    re.compile(r"""_\("((?:[^"\\]|\\.)*)"\)"""),
]


def collect():
    found = {}
    for path in (ROOT / "templates").rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        for pattern in TEMPLATE_PATTERNS:
            for m in pattern.finditer(text):
                found.setdefault(m.group(1), set()).add(str(path.relative_to(ROOT)))
    for app in ("accounts", "learning", "core", "care"):
        for path in (ROOT / app).rglob("*.py"):
            if "migrations" in path.parts or "management" in path.parts or path.name == "demo_content.py":
                continue
            # The AST joins implicitly concatenated literals, so multi-line help texts are found too.
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "_"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    found.setdefault(node.args[0].value, set()).add(str(path.relative_to(ROOT)))
    return found


def main():
    found = collect()
    if "--list" in sys.argv:
        for msgid in sorted(found):
            print(msgid)
        return
    catalog = dict(EXTRA)
    catalog.update(TRANSLATIONS)
    missing = [m for m in found if m not in catalog]
    for i, lang in enumerate(LANGS):
        po = polib.POFile()
        po.metadata = {
            "Project-Id-Version": "ruhiyat",
            "Language": lang,
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=UTF-8",
            "Content-Transfer-Encoding": "8bit",
            "Plural-Forms": PLURALS[lang],
        }
        for msgid in sorted(set(found) | set(EXTRA)):
            if msgid in catalog:
                po.append(polib.POEntry(msgid=msgid, msgstr=catalog[msgid][i]))
        for msgid, (plural, *forms) in PLURAL.items():
            po.append(polib.POEntry(msgid=msgid, msgid_plural=plural, msgstr_plural=dict(enumerate(forms[i]))))
        out = ROOT / "locale" / lang / "LC_MESSAGES" / "django.po"
        out.parent.mkdir(parents=True, exist_ok=True)
        po.save(str(out))
        print(f"{out.relative_to(ROOT)}: {len(po)} entries")
    unused = [m for m in TRANSLATIONS if m not in found]
    if unused:
        print(f"\n{len(unused)} unused translation(s):", *unused, sep="\n  ")
    if missing:
        print(f"\nMISSING {len(missing)} translation(s):", *sorted(missing), sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
