#!/usr/bin/env python3
"""
validate-locales.py — Key-parity checker for Battle Pet Utility locale modules.

Reads enUS.lua as the canonical key set, then verifies that every other
locale file in locales/ contains the same set of keys.

Usage:
    python3 scripts/validate-locales.py
"""

import re
import sys
from pathlib import Path

LOCALES_DIR = Path(__file__).parent.parent / "locales"
BASE_LOCALE = "enUS"


def extract_keys(path: Path) -> set:
    """Extract all L["key"] = "value" patterns from a Lua file."""
    keys = set()
    content = path.read_text(encoding="utf-8")
    for m in re.finditer(r'L\["([^"]+)"\]\s*=', content):
        keys.add(m.group(1))
    return keys


def main() -> int:
    base_path = LOCALES_DIR / f"{BASE_LOCALE}.lua"
    if not base_path.exists():
        print(f"ERROR: {base_path} not found", file=sys.stderr)
        return 1

    base_keys = extract_keys(base_path)
    print(f"Reference locale {BASE_LOCALE}: {len(base_keys)} keys")

    all_ok = True
    for locale_file in sorted(LOCALES_DIR.glob("*.lua")):
        name = locale_file.stem
        keys = extract_keys(locale_file)
        missing = base_keys - keys
        extra = keys - base_keys

        if missing or extra:
            all_ok = False
            print(f"\n{name}: MISMATCH")
            if missing:
                print(f"  Missing {len(missing)} keys:")
                for k in sorted(missing):
                    print(f"    - {k}")
            if extra:
                print(f"  Extra {len(extra)} keys (not in {BASE_LOCALE}):")
                for k in sorted(extra):
                    print(f"    + {k}")
        else:
            print(f"  {name}: OK ({len(keys)} keys)")

    if all_ok:
        print(f"\nAll locale files are in sync with {BASE_LOCALE}.lua")
        return 0
    else:
        print(f"\nFix the mismatches above, then re-run.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
