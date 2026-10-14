#!/usr/bin/env python3
"""
validate-locales.py — Key-parity and value-authenticity checker for Battle Pet
Utility locale modules.

Reads enUS.lua as the canonical key set, then verifies that every other
locale file in locales/ contains the same set of keys.

Value-authenticity report: counts, per locale, how many values are
byte-identical to the enUS value for the same key, and lists those keys.
The documented loanword allowlist (keys expected to stay identical to enUS
across all locales) is reported separately and does NOT fail validation.
Any key identical to enUS that is NOT in the allowlist fails validation.

Usage:
    python3 scripts/validate-locales.py
"""

import re
import sys
from pathlib import Path

LOCALES_DIR = Path(__file__).parent.parent / "locales"
BASE_LOCALE = "enUS"

# Documented loanword allowlist: keys that stay byte-identical to enUS in
# every locale. Mirrors the deDE/esES/frFR precedent (13 keys max per the
# issue-9 acceptance criteria): brand string, pure numeric/format-only
# values, single header glyphs, English debug diagnostics (a family-wide
# non-goal), and true cognates whose native spelling matches English.
ALLOWLIST = {
    "battle_pet_hud",           # brand string
    "collected_count",          # "%d / %d" numeric format
    "debug_combat_summon_blocked",
    "debug_combat_summon_resume",
    "debug_dismount_summon_blocked",
    "debug_loadout_refresh_failed",
    "header_close",             # "x"
    "header_maximize",          # "+"
    "header_minimize",          # "-"
    "pet_charms_total",          # "Total" — native word in esES/esMX/frFR/ptBR/ptPT
    "progress_percent",         # "%d%%"
    "slot_format",              # "Slot %d" — "Slot" is the gaming loanword in deDE/itIT
    "version_label",            # "Version:" label + color wrap (loanword)
    "zone_label",               # "Zone" — identical native spelling in deDE/frFR
}

# Values that are pure format/brand glyphs or numeric-only are exempt even
# outside the allowlist: they carry no translatable English text.
FORMAT_ONLY_RE = re.compile(r"^(?:\|cff[0-9a-fA-F]{8}|\|r|%[a-zA-Z]|[\s\d./:+\-x])*$")


def extract_pairs(path: Path) -> dict:
    """Extract all L["key"] = "value" pairs from a Lua file, in file order."""
    pairs = {}
    content = path.read_text(encoding="utf-8")
    for m in re.finditer(r'L\["([^"]+)"\]\s*=\s*"((?:[^"\\]|\\.)*)"', content):
        pairs[m.group(1)] = m.group(2)
    return pairs


def extract_keys(path: Path) -> set:
    """Extract all L["key"] = "value" patterns from a Lua file."""
    keys = set()
    content = path.read_text(encoding="utf-8")
    for m in re.finditer(r'L\["([^"]+)"\]\s*=', content):
        keys.add(m.group(1))
    return keys


def is_format_only(value: str) -> bool:
    """True when the value contains no translatable words, only markup/format."""
    return bool(FORMAT_ONLY_RE.match(value))


def main() -> int:
    base_path = LOCALES_DIR / f"{BASE_LOCALE}.lua"
    if not base_path.exists():
        print(f"ERROR: {base_path} not found", file=sys.stderr)
        return 1

    base_pairs = extract_pairs(base_path)
    base_keys = set(base_pairs)
    print(f"Reference locale {BASE_LOCALE}: {len(base_keys)} keys")
    print(f"Documented loanword allowlist ({len(ALLOWLIST)} keys): "
          + ", ".join(sorted(ALLOWLIST)))

    all_ok = True
    print("\nKey parity:")
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

    print("\nValue-authenticity report (values byte-identical to "
          f"{BASE_LOCALE}):")
    for locale_file in sorted(LOCALES_DIR.glob("*.lua")):
        name = locale_file.stem
        if name == BASE_LOCALE:
            continue
        pairs = extract_pairs(locale_file)
        identical = {k for k in pairs
                     if k in base_pairs and pairs[k] == base_pairs[k]}
        allowlisted = sorted(identical & ALLOWLIST)
        unlisted = sorted(
            k for k in (identical - ALLOWLIST)
            if not is_format_only(base_pairs[k])
        )
        status = "OK" if not unlisted else "FAIL"
        print(f"  {name}: {len(identical)} identical-to-{BASE_LOCALE} values "
              f"({len(allowlisted)} allowlisted, {len(unlisted)} outside "
              f"allowlist) [{status}]")
        if unlisted:
            all_ok = False
            for k in unlisted:
                print(f"    ! {k} is identical to {BASE_LOCALE} but not in "
                      f"the allowlist")

    if all_ok:
        print(f"\nAll locale files are in sync with {BASE_LOCALE}.lua and "
              f"carry genuine translations outside the documented allowlist.")
        return 0
    else:
        print("\nFix the mismatches above, then re-run.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
