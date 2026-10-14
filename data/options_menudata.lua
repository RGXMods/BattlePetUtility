local ADDON_NAME, addon = ...
local E = addon.E
local PetBattles = _G.RGXFramework:GetPetBattles()

local Fonts = _G.RGXFonts

local function NormalizeUtilityMenuState(state)
	state = tonumber(state) or 0
	state = math.floor(state)
	if state < 0 or state > 3 then
		state = 0
	end
	return state
end

function addon:GetPetItemsUtilityMenuData()
	local menu = {}
	tinsert(menu, { text = BPU.L["pet_items_options"], isTitle = true, notCheckable = true })

	if type(addon.GetPetItemCategoryMenuData) == "function" then
		local categories = addon:GetPetItemCategoryMenuData(false)
		if type(categories) == "table" then
			for _, entry in ipairs(categories) do
				tinsert(menu, entry)
			end
		end
	end
	return menu
end

function addon:GetPrimaryMenuData()
	if type(addon.PrepareFontMenuItems) == "function" then
		addon:PrepareFontMenuItems()
	end

	local sharedMediaBarTextures = {}
	for _, statusbar in ipairs(addon:ListMedia("statusbar")) do
		local barName = statusbar
		tinsert(sharedMediaBarTextures, {
			text = barName,
			func = function()
				self.db.global.barTexture = barName
				addon:RefreshMedia()
				addon.RefreshDropdownMenu(addon.ContextMenu)
			end,
			checked = function() return self.db.global.barTexture == barName end,
			keepShownOnClick = true,
			onEnter = function() addon:RefreshMedia(nil, barName) end,
			onLeave = function() addon:RefreshMedia(nil, self.db.global.barTexture) end,
		})
	end

	local _fontLabel = "Default"
	if Fonts and type(Fonts.NormalizeStyle) == "function" and type(Fonts.GetDropdownFontLabel) == "function" then
		local _style = Fonts:NormalizeStyle(self.db and self.db.global and self.db.global.normalText)
		if _style and _style.font then
			_fontLabel = Fonts:GetDropdownFontLabel(_style.font)
		end
	end

	local data = {
		{
			text = BPU.L["options_title"], isTitle = true, notCheckable = true,
		},
		{
			text = BPU.L["options_subtitle"], isTitle = true, notCheckable = true, disabled = true,
		},
		{
			text = BPU.L["lock_bpu"],
			func = function() self.db.global.IsFrameLocked = not self.db.global.IsFrameLocked end,
			checked = function() return self.db.global.IsFrameLocked end,
			isNotRadio = true,
			keepShownOnClick = true,
		},
		{
			text = BPU.L["hide_in_combat"],
			func = function() self.db.global.HideInCombat = not self.db.global.HideInCombat end,
			checked = function() return self.db.global.HideInCombat end,
			isNotRadio = true,
			keepShownOnClick = true,
		},
		{
			text = BPU.L["show_welcome"],
			func = function()
				self.db.global.ShowWelcomeMessage = not self.db.global.ShowWelcomeMessage
			end,
			checked = function() return self.db.global.ShowWelcomeMessage end,
			isNotRadio = true,
			keepShownOnClick = true,
		},
		{
			text = "", isTitle = true, notCheckable = true, disabled = true,
		},
		{
			text = BPU.L["automation"], isTitle = true, notCheckable = true,
		},
		{
			text = BPU.L["pet_battle_behavior"],
			notCheckable = true,
			hasArrow = true,
			keepShownOnClick = true,
			menuList = {
				{
					text = BPU.L["show"],
					func = function()
						self.db.global.PetBattleVisiblityMode = E.VISIBILITY_MODE.SHOW
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.PetBattleVisiblityMode == E.VISIBILITY_MODE.SHOW end,
					keepShownOnClick = true,
				},
				{
					text = BPU.L["hide"],
					func = function()
						self.db.global.PetBattleVisiblityMode = E.VISIBILITY_MODE.HIDE
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.PetBattleVisiblityMode == E.VISIBILITY_MODE.HIDE end,
					keepShownOnClick = true,
				},
				{
					text = BPU.L["do_nothing"],
					func = function()
						self.db.global.PetBattleVisiblityMode = E.VISIBILITY_MODE.DO_NOTHING
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.PetBattleVisiblityMode == E.VISIBILITY_MODE.DO_NOTHING end,
					keepShownOnClick = true,
				},
			},
		},
		{
			text = BPU.L["always_resummon"],
			func = function()
				self.db.global.AutoSummonPet = not self.db.global.AutoSummonPet
				addon:UpdateDatabrokerText()
				if self.db.global.AutoSummonPet then
					addon:UpdateAutoResummon(true)
				end
			end,
			checked = function() return self.db.global.AutoSummonPet end,
			isNotRadio = true,
			keepShownOnClick = true,
			hasArrow = true,
			menuList = {
				{ text = BPU.L["resummon_options"], isTitle = true, notCheckable = true },
				{
					text = BPU.L["last_used_pet"],
					func = function()
						self.db.global.AutoSummonMode = E.AUTO_SUMMON_MODE.LAST_PET
						addon:UpdateAutoResummon(true)
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.AutoSummonMode == E.AUTO_SUMMON_MODE.LAST_PET end,
					keepShownOnClick = true,
				},
				{
					text = BPU.L["random_favorite_pet"],
					func = function()
						self.db.global.AutoSummonMode = E.AUTO_SUMMON_MODE.FAVORITE
						addon:UpdateAutoResummon(true)
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.AutoSummonMode == E.AUTO_SUMMON_MODE.FAVORITE end,
					keepShownOnClick = true,
				},
				{
					text = BPU.L["any_random_pet"],
					func = function()
						self.db.global.AutoSummonMode = E.AUTO_SUMMON_MODE.ANY
						addon:UpdateAutoResummon(true)
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.AutoSummonMode == E.AUTO_SUMMON_MODE.ANY end,
					keepShownOnClick = true,
				},
			},
		},
		{
			text = BPU.L["auto_heal_pets"],
			func = function() self.db.global.AutoHealPets = not self.db.global.AutoHealPets; AutoHealButton_OnShow(BattlePetUtilityAutoHealButton) end,
			checked = function() return self.db.global.AutoHealPets end,
			isNotRadio = true,
			keepShownOnClick = true,
			hasArrow = true,
			menuList = {
				{ text = BPU.L["auto_pet_healer"], isTitle = true, notCheckable = true },
				{
					text = BPU.L["auto_heal_fee"],
					func = function() self.db.global.AutoHealPetsFee = not self.db.global.AutoHealPetsFee end,
					checked = function() return self.db.global.AutoHealPetsFee end,
					isNotRadio = true,
					keepShownOnClick = true,
				},
			}
		},
		{
		{
			text = "", isTitle = true, notCheckable = true, disabled = true,
		},
		{
			text = BPU.L["displays"], isTitle = true, notCheckable = true,
		},
		{
			text = BPU.L["show_main_gui"],
			func = function()
				self.db.global.HideMainGUI = not self.db.global.HideMainGUI
				addon:UpdateMinimizeState()
			end,
			checked = function() return not self.db.global.HideMainGUI end,
			isNotRadio = true,
			keepShownOnClick = true,
		},
		{
			text = BPU.L["show_zone_tracker"],
			func = function()
				self.db.global.ShowZoneTracker = not self.db.global.ShowZoneTracker
				addon:RestoreSavedSettings()
			end,
			checked = function() return self.db.global.ShowZoneTracker end,
			isNotRadio = true,
			hasArrow = true,
			keepShownOnClick = true,
			menuList = {
				{ text = BPU.L["zone_tracker_options"], isTitle = true, notCheckable = true },
				{
					text = BPU.L["show_missing_pets"],
					func = function()
						self.db.global.ShowZoneTrackerPetList = not self.db.global.ShowZoneTrackerPetList
						addon:RefreshZoneTracker()
					end,
					checked = function() return self.db.global.ShowZoneTrackerPetList end,
					isNotRadio = true,
					keepShownOnClick = true,
				},
			},
		},
		{
			text = BPU.L["show_pet_stats"],
			func = function() self.db.global.PetStatsText.Enabled = not self.db.global.PetStatsText.Enabled; addon:RestoreSavedSettings() end,
			checked = function() return self.db.global.PetStatsText.Enabled end,
			isNotRadio = true,
			keepShownOnClick = true,
			hasArrow = true,
			menuList = {
				{ text = BPU.L["health_text"], notCheckable = true, isTitle = true },
				{
					text = BPU.L["show_percentage"],
					func = function() self.db.global.PetStatsText.ShowHealthPercentage = not self.db.global.PetStatsText.ShowHealthPercentage; addon:UpdatePets() end,
					checked = function() return self.db.global.PetStatsText.ShowHealthPercentage end,
					isNotRadio = true,
					keepShownOnClick = true,
				},
				{ text = "", isTitle = true, notCheckable = true, disabled = true },
				{ text = BPU.L["experience_text"], notCheckable = true, isTitle = true },
				{
					text = BPU.L["show_percentage"],
					func = function() self.db.global.PetStatsText.ShowExperiencePercentage = not self.db.global.PetStatsText.ShowExperiencePercentage; addon:UpdatePets() end,
					checked = function() return self.db.global.PetStatsText.ShowExperiencePercentage end,
					isNotRadio = true,
					keepShownOnClick = true,
				},
				{
					text = BPU.L["show_current_exp"],
					func = function()
						self.db.global.PetStatsText.RemainingExperience = false
						addon:UpdatePets()
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return not self.db.global.PetStatsText.RemainingExperience end,
					keepShownOnClick = true,
				},
				{
					text = BPU.L["show_exp_to_level"],
					func = function()
						self.db.global.PetStatsText.RemainingExperience = true
						addon:UpdatePets()
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.PetStatsText.RemainingExperience end,
					keepShownOnClick = true,
				},
			},
		},
		{
			text = BPU.L["show_pet_charms"],
			func = function()
				self.db.global.ShowPetCharms = not self.db.global.ShowPetCharms
				addon:RestoreSavedSettings()
			end,
			checked = function() return self.db.global.ShowPetCharms end,
			isNotRadio = true,
			keepShownOnClick = true,
		},
		{
			text = BPU.L["show_pet_loadouts"],
			func = function()
				local state = tonumber(self.db.global.PetUtilityMenuState) or 0
				state = math.floor(state)
				if state < 0 or state > 3 then state = 0 end
				local hasLoadouts = (state == 2 or state == 3)
				if hasLoadouts then state = state - 2 else state = state + 2 end
				self.db.global.PetUtilityMenuState = state
				addon:RestoreSavedSettings()
			end,
			checked = function()
				local state = tonumber(self.db.global.PetUtilityMenuState) or 0
				return state == 2 or state == 3
			end,
			disabled = PetBattles:IsInBattle(),
			isNotRadio = true,
			keepShownOnClick = true,
		},
		{
			text = BPU.L["show_pet_items"],
			func = function()
				local state = NormalizeUtilityMenuState(self.db.global.PetUtilityMenuState)
				local hasItems = (state == 1 or state == 3)
				if hasItems then state = state - 1 else state = state + 1 end
				self.db.global.PetUtilityMenuState = state
				addon:RestoreSavedSettings()
			end,
			checked = function()
				local state = NormalizeUtilityMenuState(self.db.global.PetUtilityMenuState)
				return state == 1 or state == 3
			end,
			isNotRadio = true,
			hasArrow = true,
			keepShownOnClick = true,
			disabled = PetBattles:IsInBattle(),
			menuList = addon:GetPetItemsUtilityMenuData(),
		},
		{
			text = BPU.L["show_pet_tooltips"],
			func = function() self.db.global.ShowPetTooltips = not self.db.global.ShowPetTooltips end,
			checked = function() return self.db.global.ShowPetTooltips end,
			isNotRadio = true,
			keepShownOnClick = true,
		},
		},
		{
			text = BPU.L["show_pepe"],
			func = function()
				self.db.global.ShowPepe = not self.db.global.ShowPepe
				addon:RefreshHeaderArt()
				if self.db.global.ShowPepe then
					BattlePetUtilityFrameTitle.pepeFrame:Show()
				else
					BattlePetUtilityFrameTitle.pepeFrame:Hide()
				end
			end,
			checked = function() return self.db.global.ShowPepe end,
			isNotRadio = true,
			hasArrow = true,
			keepShownOnClick = true,
			menuList = {
				{ text = BPU.L["pepe_position"], notCheckable = true, isTitle = true },
				{
					text = BPU.L["right_side"],
					func = function()
						self.db.global.PepeOnLeft = false
						addon:RefreshHeaderArt()
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return not self.db.global.PepeOnLeft end,
					keepShownOnClick = true,
				},
				{
					text = BPU.L["left_side"],
					func = function()
						self.db.global.PepeOnLeft = true
						addon:RefreshHeaderArt()
						addon.RefreshDropdownMenu(addon.ContextMenu)
					end,
					checked = function() return self.db.global.PepeOnLeft end,
					keepShownOnClick = true,
				},
			},
		},
		{
			text = BPU.L["show_minimap_icon"],
			func = function()
				if type(addon.ToggleMinimapIcon) == "function" then
					addon:ToggleMinimapIcon(nil)
				end
			end,
			checked = function()
				return self.db.global.MinimapIcon and self.db.global.MinimapIcon.enabled
			end,
			isNotRadio = true,
			keepShownOnClick = true,
			tooltipTitle = BPU.L["minimap_icon_visibility"],
			tooltipText = BPU.L["minimap_icon_tooltip"],
		},
		{
			text = "", isTitle = true, notCheckable = true, disabled = true,
		},
		{
			text = BPU.L["frame_options"], isTitle = true, notCheckable = true, disabled = true,
		},
		{
			text = BPU.L["font_label"] .. _fontLabel,
			notCheckable = true,
			hasArrow = true,
			menuList = "bpu_fonts",
		},
		{
			text = string.format(BPU.L["font_size_format"], addon:GetCurrentFontSize()),
			notCheckable = true,
			hasArrow = true,
			keepShownOnClick = true,
			menuList = addon:GetTextSizeMenuData(),
		},
		{
			text = BPU.L["bar_texture"],
			notCheckable = true,
			hasArrow = true,
			menuList = sharedMediaBarTextures,
		},
		{
			text = string.format(BPU.L["change_scale_format"], self.db.global.WindowScale * 100),
			notCheckable = true,
			hasArrow = true,
			keepShownOnClick = true,
			menuList = addon:GetWindowScaleMenu(),
		},
		{
			text = string.format(BPU.L["window_opacity_format"], math.floor((self.db.global.WindowOpacity or 1.0) * 100 + 0.5)),
			notCheckable = true,
			hasArrow = true,
			keepShownOnClick = true,
			menuList = addon:GetWindowOpacityMenu(),
		},
		{
			text = BPU.L["show_title_backdrop"],
			func = function()
				self.db.global.TitleBackdrop = not self.db.global.TitleBackdrop
				addon:ApplyTitleBackdrop()
			end,
			checked = function() return self.db.global.TitleBackdrop end,
			isNotRadio = true,
			keepShownOnClick = true,
		},
	}

	return data
end
