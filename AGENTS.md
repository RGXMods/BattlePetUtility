# BattlePetUtility

BattlePetUtility is a Retail-only WoW addon for battle-pet loadouts, pet-related action buttons, healing, summoning, zone tracking, and options. `BattlePetUtility.toc` is the authoritative metadata and load list; it currently targets Retail interface `120007` and requires `RGX-Framework`.

## Layout

- `data/` contains runtime Lua modules. Keep their TOC order intact when adding dependencies between modules.
- `ui/` contains the XML templates and frames loaded after the Lua modules.
- `media/` contains shipped textures and icons.
- `docs/CHANGES.md` is the canonical changelog; `docs/RELEASING.md` and `docs/ROADMAP.md` contain supporting release and planning notes.

## Framework Rules

- Use the existing RGX APIs for lifecycle events, timers, hooks, slash commands, the database, minimap integration, and debug output rather than introducing parallel plumbing.
- The RGXPetBattles migration is complete: battle-pet operations use `RGX:GetPetBattles()`. Do not reintroduce direct `C_PetBattles` calls.
- The RGXDropdowns migration is complete for addon context menus: `data/options_dropdown.lua` uses `RGXDropdowns:CreateContextMenu`. Preserve the legacy menu-item schema consumed by that adapter.
- `data/itembuttons.lua` must not change secure button attributes during combat. Preserve `SafeSetButtonAttribute` and the deferred `PLAYER_REGEN_ENABLED` refresh path.
- Keep aura checks on `C_UnitAuras.GetPlayerAuraBySpellID`; do not inspect secret aura fields.
- Framework references: `../RGX-Framework/AGENTS.md`, `../RGX-Framework/docs/API.md`, and `../RGX-Framework/docs/DROPDOWNS.md`.

## Development And Release

- Match the existing tab indentation and semicolon-terminated style in `data/`.
- There is no standalone build or automated test suite. Install the repository as `BattlePetUtility` in the Retail AddOns directory, ensure `RGX-Framework` is installed, run `/reload`, and exercise the HUD, loadouts, context menus, item buttons, pet battle transitions, and combat-lockdown recovery.
- For a release, update `BattlePetUtility.toc` and the relevant documentation/changelog entries. Stable tags use `vX.Y.Z`; `.github/workflows/release.yml` validates the tag against the TOC version and packages with BigWigsMods/packager. Branch pushes to `dev` and `alpha` produce their corresponding channels.

## Repository Workflow

- The GitLab project under `rgxmods/warcraft` is authoritative. Normal work belongs on task branches and must merge through GitLab merge requests, never directly to the default branch.
- Shared CI is included from `rgxmods/warcraft/RGX-Framework` at `/.gitlab/ci/addon.yml`; validation must pass before publishing to the GitHub mirror.
- The GitHub `RGXMods` repository is downstream distribution, not development authority.
- Keep GitLab and GitHub release tags identical, and use protected GitLab release tags.
- Preserve any existing working Wago connection and ID exactly. Never create a new Wago connection without explicit user direction.
- Publishing integrations prohibited by the shared validation policy are retired and must not be restored.
- The root `README.md` must remain detailed and project-specific. Narrow distribution edits must not replace or truncate installation, features, compatibility, usage, media, or support content.
- Verify relative README assets. Do not overwrite newer compatibility facts with stale monorepo or history text.

## Building With RGX-Framework

- Contract first: build new addon behavior from the declarative `RGXAddon(name, opts)` table. Read `rgxmods/warcraft/RGX-Framework`'s `docs/DECLARATIVE-API.md` and schema before writing code; use only keys marked as shipped today. Tier 4 keys are future targets, not runtime features. Use `onInit` and addon-scoped methods when the shipped declarative surface needs an escape hatch.
- MCP tool loop: before writing UI, timers, events, auras, or slash handling, run `rgx_get_contract` -> `rgx_generate_addon` -> `rgx_validate_addon` -> `rgx_audit_lua`. Compare generated Lua with existing integration and validate the actual opts table; audit every changed Lua file. The generator is a starting point, not a replacement for project-specific behavior.
- Prefer framework-owned timers (`every`, `addon:After`, `addon:Every`), event and unit-event registration, slash commands, minimap button, saved-settings database, aura watching, UI controls and dropdowns, colors, fonts, theming, tooltips, and sound. Use the framework's shipped module APIs for advanced behavior rather than duplicating WoW plumbing. Preserve existing secure-button combat deferral, pet-battle adapter, and dropdown adapter.
- Audit failures are blockers: raw `C_Timer`, manual event frames, `SLASH_` globals, unguarded `SetAttribute`, raw aura plumbing, and reassigned hooks must be replaced with framework-managed, combat-safe equivalents. Existing compatibility paths require an explicit migration plan; do not silently break them to satisfy an audit.
- Keep `## RequiredDeps: RGX-Framework` and any `## X-RGX-Framework-MinVersion` accurate against the framework version line. Match the TOC SavedVariables name with the declarative `dbName`. Use Lua 5.1 (`luac5.1 -p`) and XML (`xmllint`) validation through the shared CI include before each MR; keep the root README nonempty and substantive.
- This addon targets Retail and uses `/bpu` for its options panel. The TOC owns its `vX.Y.Z` version and file load order. Recheck those facts in the TOC and README when they change; the earlier interface number in this document is historical.

## Keeping Interface Versions Current

- Read the game's `.build.info` in the WoW installation root immediately before changing a TOC or releasing. Its Product column identifies each installed flavor; its Version column is `major.minor.patch.build`. Derive `## Interface:` as `major * 10000 + minor * 100 + patch`: `1.60.1` -> `16001`, `1.15.9` -> `11509`, `2.5.6` -> `20506`, `5.5.4` -> `50504`. A multi-flavor addon carries a comma-separated list.
- Cross-check builds unavailable locally against `wago.tools/build` and `versions.wowtools.io` only after verifying those feeds are reachable. If a feed is unavailable, use the installed client's `.build.info` as the authoritative source; do not guess an uninstalled flavor's live version.
- A stale `## Interface:` is a bug. Fix it in a task-branch MR with passing shared CI before release. Before every commit, verify all supported interfaces, the existing version prefix/suffix scheme, dependency and minimum-version fields, the unchanged `## Author:` line, valid `## Key: value` metadata, every referenced file, and the intended root flavor TOCs. Remove retired publishing metadata while preserving existing distribution IDs that remain in use. Review added diff lines for personal or private details; the TOC `## Author:` line is the only author-information exception.
- Release through GitLab MR and green shared validation, then patch-bump through the same discipline and create a protected GitLab version tag. Verify the identical tag in the downstream `RGXMods/BattlePetUtility` mirror before reporting distribution pickup.
