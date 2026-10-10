# Localization Guide

This directory contains localization files for Battle Pet Utility. Each file
translates the addon's user interface into a specific World of Warcraft client
locale.

## Supported Locales

Battle Pet Utility currently supports all 12 World of Warcraft retail client
locales:

- **enUS** - English (United States) - *Default / Fallback*
- **deDE** - German (Deutsch)
- **esES** - Spanish (España)
- **esMX** - Latin American Spanish (Español de México)
- **frFR** - French (Français)
- **itIT** - Italian (Italiano)
- **koKR** - Korean (한국어)
- **ptBR** - Portuguese - Brazil (Português do Brasil)
- **ptPT** - Portuguese - Portugal (Português)
- **ruRU** - Russian (Русский)
- **zhCN** - Chinese (Simplified) (简体中文)
- **zhTW** - Chinese (Traditional) (繁體中文)

## How Localization Works

### For Users

The addon automatically detects your WoW client's language setting and displays
text in that language. No configuration is needed—if your WoW client is set to
French, the addon will show French text.

### For Developers

1. **String Definition**: All user-visible strings are defined in `enUS.lua`
   using a key-value structure:
   ```lua
   BPU.L["welcome_message"] = "Welcome! Use |cffb07fff/BPU|r to toggle...";
   ```

2. **Locale Loading**: Locale files are loaded via the `.toc` file in order:
   - `data/compat.lua` (sets up BPU global)
   - `locales/enUS.lua` (base locale, defines all keys)
   - Other locale files (override specific keys if locale matches)

3. **String Access**: Code accesses localized strings via `BPU.L["key"]`:
   ```lua
   print(BPU.L["welcome_message"])
   ```

### Locale File Structure

Each locale file follows this pattern:

```lua
-- Language Name
-- Translators: see CONTRIBUTING.md

local ADDON_NAME, addon = ...;

-- Only load for this specific client locale
if GetLocale() ~= "deDE" then return end

-- Create localization table if not exists
BPU = BPU or {};
BPU.L = BPU.L or {};

local L = BPU.L;

-- Override specific strings
L["welcome_message"] = "Willkommen! ...";
```

The `GetLocale()` check ensures the file only runs on matching client locales.
Keys not defined in a locale file fall back to the `enUS` value.

### Adding a New String

When adding new features that display text:

1. Add the English string to `locales/enUS.lua`
2. Add the same key to all other locale files (initially with English fallback)
3. Use `BPU.L["your_key"]` in the Lua code
4. Submit translations for the new key in a follow-up PR

### Color and Format Codes

Preserve these WoW-specific codes in translations:

- `|cffRRGGBB` ... `|r` — Text coloring
- `|n` — Newline
- `%s`, `%d` — String/number substitution
- `|h` ... `|h` — Hyperlinks

**Example:**
```lua
L["version_label"] = "|cffffff00Version:|r |cff8080ff%s|r"
```

## Contributing Translations

See [CONTRIBUTING.md](CONTRIBUTING.md) for submission guidelines.

## Validation

Run the validation script to check key parity across all locale files:

```bash
python3 scripts/validate-locales.py
```

This ensures all locale files define the same set of keys as `enUS.lua`.
