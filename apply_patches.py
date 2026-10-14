#!/usr/bin/env python3
import re
from pathlib import Path

def patch_literal_in_file(filepath, literal, key):
    """
    Replace all occurrences of "literal" with BPU.L["key"] in the given file.
    Returns True if any replacement was made.
    """
    text = filepath.read_text(encoding='utf-8')
    quoted = f'"{literal}"'
    replacement = f'BPU.L["{key}"]'
    if quoted not in text:
        return False
    new_text = text.replace(quoted, replacement)
    if new_text == text:
        return False
    filepath.write_text(new_text, encoding='utf-8')
    return True

def main():
    base = Path('/workspace/bpu-issue9-at9')
    patches = [
        # data/core.lua
        (base / 'data' / 'core.lua', '|cffffee00Slot Locked|r', 'slot_locked'),
        (base / 'data' / 'core.lua', '|cffffee00Empty Slot|r', 'empty_slot'),
        (base / 'data' / 'core.lua', 'Earn Achievement |cffffff00[Newbie]|r to Unlock This Slot', 'earn_newbie'),
        (base / 'data' / 'core.lua', 'Earn Achievement |cffffff00[Just a Pup]|r to Unlock This Slot', 'earn_pup'),
        # data/core.lua HUD tooltips (already done? but we'll ensure)
        (base / 'data' / 'core.lua', 'Restore Battle Pet Utility|cffb512fc!|r', 'hud_restore'),
        (base / 'data' / 'core.lua', 'Show the full battle pet HUD.', 'hud_restore_help'),
        (base / 'data' / 'core.lua', 'Minimize Battle Pet Utility|cffb512fc!|r', 'hud_minimize'),
        (base / 'data' / 'core.lua', 'Collapse to the title bar.', 'hud_minimize_help'),
        # data/zonetracking.lua
        (base / 'data' / 'zonetracking.lua', 'All zone pets collected', 'zone_pets_collected'),
        # data/petloadouts.lua
        (base / 'data' / 'petloadouts.lua', 'Another loadout with the same name already exists. Do you want to overwrite?', 'loadout_overwrite_confirm'),
        (base / 'data' / 'petloadouts.lua', 'Load (Rematch)', 'load_rematch_team'),
        (base / 'data' / 'petloadouts.lua', 'Restore', 'restore_loadout'),
        (base / 'data' / 'petloadouts.lua', 'No loadouts', 'no_loadouts'),
        (base / 'data' / 'petloadouts.lua', 'No Results', 'no_results'),
        (base / 'data' / 'petloadouts.lua', 'Pet #%d not found', 'pet_not_found'),
        (base / 'data' / 'petloadouts.lua', 'Heal pets spell', 'heal_pets_spell'),
        (base / 'data' / 'petloadouts.lua', 'Battle bandage', 'battle_bandage'),
        # data/itembuttons.lua
        (base / 'data' / 'itembuttons.lua', 'Battle Stones', 'battle_stones'),
        (base / 'data' / 'itembuttons.lua', 'Pet quality and level-up stones', 'battle_stones_tooltip'),
        (base / 'data' / 'itembuttons.lua', 'Consumables and toys', 'consumables_and_toys'),
        (base / 'data' / 'itembuttons.lua', 'Treats, utility items, toys, and costumes', 'consumables_tooltip'),
        (base / 'data' / 'itembuttons.lua', 'Supply bags and containers', 'supply_bags_containers'),
        (base / 'data' / 'itembuttons.lua', 'Pet supply bags and battle pet container items', 'supply_bags_tooltip'),
        (base / 'data' / 'itembuttons.lua', 'Pet currencies', 'pet_currencies'),
        (base / 'data' / 'itembuttons.lua', 'Charm and pet-related currency items', 'pet_currencies_tooltip'),
        # data/options_menudata.lua
        (base / 'data' / 'options_menudata.lua', 'Minimap icon visibility', 'minimap_icon_visibility'),
        (base / 'data' / 'options_menudata.lua', 'You can also right-click the minimap button for options, or use |cffb07fff/BPU icon off|r and |cffb07fff/BPU icon on|r.', 'minimap_icon_tooltip'),
        # data/pethealer.lua
        (base / 'data' / 'pethealer.lua', 'Heal and Revive Pets (%s / %d wounded)', 'heal_and_revive_pets'),
        (base / 'data' / 'pethealer.lua', 'Heal and Revive Pets (free / %d wounded)', 'heal_and_revive_free'),
        # data/options_menudata.lua font/size/scale/opacity (these are not literals but we can still replace the format strings)
        (base / 'data' / 'options_menudata.lua', 'Font: ', 'font_label'),  # This is part of a concatenation; we need to be careful.
        (base / 'data' / 'options_menudata.lua', 'Font size (%d pt)', 'font_size_format'),
        (base / 'data' / 'options_menudata.lua', 'Change scale (%d%%)', 'change_scale_format'),
        (base / 'data' / 'options_menudata.lua', 'Window opacity (%d%%)', 'window_opacity_format'),
        # data/zonetracking.lua more strings
        (base / 'data' / 'zonetracking.lua', ', +', 'more_format_summary'),  # part of a concatenation
        (base / 'data' / 'zonetracking.lua', '+%d more', 'more_format_tooltip'),
        (base / 'data' / 'zonetracking.lua', ' +', 'more_format_line'),  # part of a concatenation
        (base / 'data' / 'zonetracking.lua', 'Map data unavailable on this client.', 'map_data_unavailable'),
        (base / 'data' / 'zonetracking.lua', 'No trackable wild pets found for this zone.', 'no_trackable_wild_pets'),
        # data/databroker.lua
        (base / 'data' / 'databroker.lua', 'Unknown Pet', 'unknown_pet'),
        (base / 'data' / 'databroker.lua', 'Species ', 'species_prefix'),
        (base / 'data' / 'databroker.lua', '|cffff5555wounded|r', 'wounded_format'),
        (base / 'data' / 'databroker.lua', 'Battle Pet Utility!', 'addon_title'),
        # data/core.lua chat prints
        (base / 'data' / 'core.lua', 'Welcome! Use |cffb07fff/BPU|r to toggle, and |cffb07fff/BPU help|r for commands.', 'welcome_message'),
        (base / 'data' / 'core.lua', '|cffffff00Version:|r |cff8080ff%s|r', 'version_label'),
        (base / 'data' / 'core.lua', '|cff00ff00Welcome message enabled.|r', 'welcome_enabled'),
        (base / 'data' / 'core.lua', '|cffff0000Welcome message disabled.|r', 'welcome_disabled'),
        (base / 'data' / 'core.lua', '|cffb07fff/BPU|r - Toggle Battle Pet Utility|cffb512fc!|r', 'hud_toggle'),
        (base / 'data' / 'core.lua', ' |cffb07fff/BPU help|r - Show command help', 'help_help'),
        (base / 'data' / 'core.lua', ' |cffb07fff/BPU icon on|r or |cffb07fff/BPU icon off|r - Show/hide minimap icon', 'help_icon'),
        (base / 'data' / 'core.lua', ' |cffb07fff/BPU welcome|r - Toggle login welcome message', 'help_welcome'),
        (base / 'data' / 'core.lua', ' |cffb07fff/BPU version|r - Show current version', 'help_version'),
        (base / 'data' / 'core.lua', '|cffffcc00Minimap icon hidden.|r Use |cffb07fff/BPU icon on|r to show it again.', 'minimap_hidden'),
        (base / 'data' / 'core.lua', '|cff00ff00Minimap icon shown.|r', 'minimap_shown'),
        # ui/BattlePetUtilityFrame.xml
        (base / 'ui' / 'BattlePetUtilityFrame.xml', 'Auto Heal Pets', 'auto_heal_pets_button'),
    ]

    total_patched = 0
    for filepath, literal, key in patches:
        if patch_literal_in_file(filepath, literal, key):
            total_patched += 1
            print(f'Patched: {filepath.relative_to(base)}: "{literal[:30]}..." -> BPU.L["{key}"]')
        else:
            # Check if the literal might be split across lines or have different quoting
            pass
    print(f'\nTotal patches applied: {total_patched}')

if __name__ == '__main__':
    main()