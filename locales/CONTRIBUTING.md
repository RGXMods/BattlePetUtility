# Contributing Translations

Localization files for Battle Pet Utility live in this directory (`locales/`).

## File layout

| File       | Purpose                                                          |
|------------|------------------------------------------------------------------|
| `enUS.lua` | Base locale — always loaded, provides all keys and defaults.     |
| `deDE.lua` | German                                                           |
| `esES.lua` | Spanish (Spain)                                                  |
| `esMX.lua` | Latin American Spanish                                           |
| `frFR.lua` | French                                                         |
| `itIT.lua` | Italian                                                        |
| `koKR.lua` | Korean                                                         |
| `ptBR.lua` | Brazilian Portuguese                                              |
| `ptPT.lua` | European Portuguese                                               |
| `ruRU.lua` | Russian                                                        |
| `zhCN.lua` | Simplified Chinese                                                |
| `zhTW.lua` | Traditional Chinese                                              |

## Adding a new locale

1. Copy the structure of `deDE.lua` (a real-translation sample).
2. Name the file with the [WoW locale code](https://wowpedia.fandom.com/wiki\Locales)
   (e.g. `enGB.lua` for British English).
3. Change the `GetLocale()` guard to match your locale code.
4. Translate every key — keep the **same set of keys** as `enUS.lua`.
   Un-translated keys silently fall back to the `enUS` string at runtime.
5. Add the file to `BattlePetUtility.toc` in the correct load-order position
   (after `enUS.lua`, after all data modules).
6. Add the locale to the `## X-Localizations:` field in the TOC.

## Translation rules

- **Never change keys** — add, remove, or rename keys must be done across
  **all** locale files simultaneously.  A missing key in any locale file
  causes a `nil` at runtime (add-on will error).
- **Preserve `|r` color codes** and `{brace}` escape sequences exactly.
- **Preserve `%s`, `%d`, `%.2f`, and `|n` placeholders** verbatim.
- **Single double-quotes inside strings must be escaped** as `\"`.
- Use the **validation script** in the repository root to verify key parity
  across all locale files before submitting:

```
python3 scripts/validate-locales.py
```

## Running the parity checker

The checker verifies that every locale file (except `enUS.lua`) contains
the same set of keys as `enUS.lua`.  Run it from the repository root:

```
python3 scripts/validate-locales.py
```

Exit code 0 means all locale files are in sync.  Any missing or extra keys
are reported with file and line numbers.
