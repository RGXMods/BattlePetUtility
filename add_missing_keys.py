#!/usr/bin/env python3
import re
import os
from pathlib import Path

def extract_keys(path):
    text = path.read_text(encoding='utf-8')
    # pattern matches L["key"] = "value"; or L["key"] = "value"
    pattern = r'L\["([^"]+)"\]\s*=\s*"((?:[^"\\]|\\.)*)"'
    return dict(re.findall(pattern, text))

locales_dir = Path('/workspace/bpu-issue9-at9/locales')
enUS_path = locales_dir / 'enUS.lua'
enUS_keys = extract_keys(enUS_path)
print(f'enUS has {len(enUS_keys)} keys')

for locale_file in sorted(locales_dir.glob('*.lua')):
    if locale_file.stem == 'enUS':
        continue
    keys = extract_keys(locale_file)
    missing = [k for k in enUS_keys if k not in keys]
    if not missing:
        print(f'{locale_file.name}: OK (no missing)')
        continue
    # Build lines to append
    lines = []
    for k in missing:
        v = enUS_keys[k]
        v_esc = v.replace('\\', '\\\\').replace('"', '\\"')
        lines.append(f'L["{k}"] = "{v_esc}";')
    # Append
    with locale_file.open('a', encoding='utf-8') as f:
        if not lines:
            continue
        # Ensure we end with newline before appending
        f.write('\n')
        f.write('\n'.join(lines) + '\n')
    print(f'{locale_file.name}: added {len(lines)} missing keys')