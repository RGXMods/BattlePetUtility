# Unreleased

## Changes

- Display options reorganized: visibility toggles now live under Displays (including the moved main-body and minimap controls), with the double-negative Hide main GUI body replaced by Show main GUI body.
- Added window opacity (50-100%, hover-previewed) and a Show title bar backdrop toggle under Frame Options.
- Header decoration options renamed to plain language: Show Pepe (cuteness) and Pepe position.
# v2.3.24 - 2026-09-27

## Changes

- Text size options now live-preview on hover. Hover previews now cover font, bar texture, and text size selections in the /bpu menu.
- Removed the retired third-party directory listing; distribution is CurseForge and GitHub only.
- MIT license added.
- Project documentation restored and aligned with the CurseForge description.

# v2.3.22 - 2026-08-13

## Changes

- Battle-pet operations migrated to RGXPetBattles (`RGX:GetPetBattles()`); direct C_PetBattles calls removed.

# v2.3.21 - 2026-08-08

## Changes
- **Minimap API update**: `RGX:CreateMinimapButton()` → `RGXMinimap:Create()` (new API)
- Slash commands already use `RGX:RegisterSlashCommand`
- Database already uses `RGX:NewDatabase()`
- Options context menus migrated to RGXDropdowns (custom dropdown) with hover live previews for font and bar texture selections.

## Fixes

- Fixed item-button secure actions not being deterministically reapplied after combat. `SafeSetButtonAttribute` correctly refuses `SetAttribute` during combat lockdown (taint-safe), but the deferred-refresh flag was never consumed and the item-button event bridge did not listen for `PLAYER_REGEN_ENABLED` — a button configured during combat only recovered incidentally on the next bag update. The bridge now listens for combat end and rebuilds the buttons when a write was deferred.

# v2.3.20 - 2026-06-30

## Fixes

- Fixed tainted aura scan — eating/combat helper now uses `C_UnitAuras.GetPlayerAuraBySpellID` instead of indexing aura slots, avoiding the secret `spellId` field that triggers hardware-event taint in combat.

# v2.3.19 - 2026-06-30

## Changes

- Updated Battle Pet Utility! for WoW Retail 12.0.7 with RGX-Framework dependency support.
- Completed PetBuddy2 to Battle Pet Utility! naming/branding cleanup across the live addon files.
- Restored HUD icon and TGA asset paths for the title, minimap, and loadout controls.

## Fixes

- Fixed broken HUD frame/icon rendering after the rename.
- Fixed BPU database initialization paths that could leave `addon.db` unavailable to frame handlers.
- Fixed tainted aura checks by avoiding secret aura-name comparisons in the eating/combat helper path.
- Fixed combat lockdown blocked action from zone tracker frame height updates.

# v2.3.18 - 2026-05-01

## Changes

- Updated BattlePetUtility font integration to use the corrected shared RGX font pipeline.
- Refreshed BattlePetUtility UI text rendering so addon panels and controls use the intended bundled font styling.
- Aligned BattlePetUtility option UI presentation with the updated RGX Framework behavior.

## Fixes

- Fixed BattlePetUtility font display issues caused by incomplete shared font registration/lookup behavior.
- Fixed inconsistent option UI text styling after the RGX font/layout updates.
