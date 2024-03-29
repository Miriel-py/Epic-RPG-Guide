# components.py
"""Contains global interaction components"""

from typing import List, Literal, Optional

import discord

from resources import emojis, strings, modals


class AreaCheckSelect(discord.ui.Select):
    """Area check select"""
    def __init__(self, active_area: int):
        options = []
        for area_no in range(1,22):
            label = f'Area {area_no}' if area_no != 21 else 'The TOP'
            emoji = '🔹' if area_no == active_area else None
            options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
        super().__init__(placeholder='Choose area ...', min_values=1, max_values=1, options=options,
                         custom_id='select_area', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_area = int(select_value)
        embed = await self.view.function_embed(self.view.active_area, self.view.user_at, self.view.user_def,
                                               self.view.user_life)
        for child in self.view.children.copy():
            if child.custom_id == 'select_area':
                self.view.remove_item(child)
                self.view.add_item(AreaCheckSelect(self.view.active_area))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_area == 21 else False
            if child.custom_id == 'prev':
                child.disabled = True if self.view.active_area == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class AreaDungeonCheckSwitchButton(discord.ui.Button):
    """Button for area/dungeon check that switches to the opposite check"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message()
        if self.custom_id == 'dungeon-switch':
            area_dungeon = float(self.view.active_area)
            function = self.view.function_dungeon_check
            function_check_switch = self.view.function_area_check
        else:
            area_dungeon = self.view.active_dungeon
            if area_dungeon.is_integer(): area_dungeon = int(self.view.active_dungeon)
            if area_dungeon == 15.2: area_dungeon = 15
            function = self.view.function_area_check
            function_check_switch = self.view.function_dungeon_check

        self.view.value = 'switched'
        self.view.stop()
        await function(self.view.bot, self.view.ctx, area_dungeon, function_check_switch, switch_view=self.view)


class AreaDungeonGuideSwitchButton(discord.ui.Button):
    """Button for area/dungeon guide that switches to the opposite guide"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message()
        if self.custom_id == 'dungeon-switch':
            area_dungeon = float(self.view.active_area)
            function = self.view.function_dungeon_guide
            function_guide_switch = self.view.function_area_guide
        else:
            area_dungeon = self.view.active_dungeon
            if area_dungeon.is_integer(): area_dungeon = int(self.view.active_dungeon)
            if area_dungeon == 15.2: area_dungeon = 15
            function = self.view.function_area_guide
            function_guide_switch = self.view.function_dungeon_guide
        self.view.value = 'switched'
        self.view.stop()
        await function(self.view.ctx, area_dungeon, function_guide_switch, switch_view=self.view)


class AreaCheckPaginatorButton(discord.ui.Button):
    """Paginator button for area check view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_area -= 1
            if self.view.active_area == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            self.view.active_area += 1
            if self.view.active_area == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_area':
                options = []
                for area_no in range(1,22):
                    label = f'Area {area_no}' if area_no != 21 else 'The TOP'
                    emoji = '🔹' if area_no == self.view.active_area else None
                    options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function_embed(self.view.active_area, self.view.user_at, self.view.user_def,
                                               self.view.user_life)
        await interaction.response.edit_message(embed=embed, view=self.view)


class AreaGuideSelect(discord.ui.Select):
    """Area guide select"""
    def __init__(self, active_area: int):
        options = []
        for area_no in range(1,22):
            label = f'Area {area_no}' if area_no != 21 else 'The TOP'
            emoji = '🔹' if area_no == active_area else None
            options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
        super().__init__(placeholder='Choose area ...', min_values=1, max_values=1, options=options,
                         custom_id='select_area', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_area = int(select_value)
        embed = await self.view.function_embed(self.view.ctx, self.view.active_area, self.view.db_user, self.view.full_guide)
        for child in self.view.children.copy():
            if child.custom_id == 'select_area':
                self.view.remove_item(child)
                self.view.add_item(AreaGuideSelect(self.view.active_area))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_area == 21 else False
            if child.custom_id == 'prev':
                child.disabled = True if self.view.active_area == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class AreaGuidePaginatorButton(discord.ui.Button):
    """Paginator button for area guide view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_area -= 1
            if self.view.active_area == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            self.view.active_area += 1
            if self.view.active_area == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_area':
                options = []
                for area_no in range(1,22):
                    label = f'Area {area_no}' if area_no != 21 else 'The TOP'
                    emoji = '🔹' if area_no == self.view.active_area else None
                    options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function_embed(self.view.ctx, self.view.active_area, self.view.db_user, self.view.full_guide)
        await interaction.response.edit_message(embed=embed, view=self.view)


class CraftingRecalculateButton(discord.ui.Button):
    """Recalculation button for the crafting calculator"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        modal = modals.CraftingCalculatorAmountModal(self.view)
        await interaction.response.send_modal(modal)


class DungeonCheckSelect(discord.ui.Select):
    """Dungeon check select"""
    def __init__(self, active_dungeon: float):
        options = []
        for dungeon_no in strings.DUNGEONS:
            label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
            label = label.replace('.','-')
            emoji = '🔹' if dungeon_no == active_dungeon else None
            options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
        super().__init__(placeholder='Choose dungeon ...', min_values=1, max_values=1, options=options,
                         custom_id='select_dungeon', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_dungeon = float(select_value)
        embed = await self.view.function_embed(self.view.active_dungeon, self.view.user_at, self.view.user_def,
                                               self.view.user_life)
        for child in self.view.children.copy():
            if child.custom_id == 'select_dungeon':
                self.view.remove_item(child)
                self.view.add_item(DungeonCheckSelect(self.view.active_dungeon))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_dungeon == 21 else False
            if child.custom_id == 'prev':
                child.disabled = True if self.view.active_dungeon == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class DungeonCheckPaginatorButton(discord.ui.Button):
    """Paginator button for dungeon check view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            if self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 15.0
            elif self.view.active_dungeon == 16:
                self.view.active_dungeon = 15.2
            else:
                self.view.active_dungeon -= 1
            if self.view.active_dungeon == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            if self.view.active_dungeon == 15:
                self.view.active_dungeon = 15.2
            elif self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 16.0
            else:
                self.view.active_dungeon += 1
            if self.view.active_dungeon == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_dungeon':
                options = []
                for dungeon_no in strings.DUNGEONS:
                    label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
                    label = label.replace('.','-')
                    emoji = '🔹' if dungeon_no == self.view.active_dungeon else None
                    options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function_embed(self.view.active_dungeon, self.view.user_at, self.view.user_def,
                                               self.view.user_life)
        await interaction.response.edit_message(embed=embed, view=self.view)


class DungeonGuideSelect(discord.ui.Select):
    """Dungeon guide select"""
    def __init__(self, active_dungeon: float):
        options = []
        for dungeon_no in strings.DUNGEONS:
            label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
            label = label.replace('.','-')
            emoji = '🔹' if dungeon_no == active_dungeon else None
            options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
        super().__init__(placeholder='Choose dungeon ...', min_values=1, max_values=1, options=options,
                         custom_id='select_dungeon', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_dungeon = float(select_value)
        embed = await self.view.function_embed(self.view.active_dungeon)
        for child in self.view.children.copy():
            if child.custom_id == 'select_dungeon':
                self.view.remove_item(child)
                self.view.add_item(DungeonGuideSelect(self.view.active_dungeon))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_dungeon == 21 else False
            if child.custom_id == 'prev':
                child.disabled = True if self.view.active_dungeon == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class DungeonGuidePaginatorButton(discord.ui.Button):
    """Paginator button for dungeon guide view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            if self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 15.0
            elif self.view.active_dungeon == 16:
                self.view.active_dungeon = 15.2
            else:
                self.view.active_dungeon -= 1
            if self.view.active_dungeon == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            if self.view.active_dungeon == 15:
                self.view.active_dungeon = 15.2
            elif self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 16.0
            else:
                self.view.active_dungeon += 1
            if self.view.active_dungeon == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_dungeon':
                options = []
                for dungeon_no in strings.DUNGEONS:
                    label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
                    label = label.replace('.','-')
                    emoji = '🔹' if dungeon_no == self.view.active_dungeon else None
                    options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function_embed(self.view.active_dungeon)
        await interaction.response.edit_message(embed=embed, view=self.view)


class TopicSelect(discord.ui.Select):
    """Topic Select"""
    def __init__(self, topics: dict, active_topic: str, placeholder: str, row: Optional[int] = None):
        self.topics = topics
        options = []
        for topic in topics.keys():
            label = topic
            emoji = '🔹' if topic == active_topic else None
            options.append(discord.SelectOption(label=label, value=label, emoji=emoji))
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options, row=row,
                         custom_id='select_topic')

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_topic = select_value
        for child in self.view.children:
            if child.custom_id == 'select_topic':
                options = []
                for topic in self.topics.keys():
                    label = topic
                    emoji = '🔹' if topic == self.view.active_topic else None
                    options.append(discord.SelectOption(label=label, value=label, emoji=emoji))
                child.options = options
                break
        embed = await self.view.topics[select_value]()
        await interaction.response.edit_message(embed=embed, view=self.view)


class PaginatorButton(discord.ui.Button):
    """Paginator button"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_page -= 1
            if self.view.active_page == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            self.view.active_page += 1
            if self.view.active_page == len(self.view.pages): self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'pages':
                child.label = f'{self.view.active_page}/{len(self.view.pages)}'
                break
        await interaction.response.edit_message(embed=self.view.pages[self.view.active_page-1], view=self.view)


class CustomButton(discord.ui.Button):
    """Custom Button. Writes its custom id to the view value and stops the view."""
    def __init__(self, style: discord.ButtonStyle, custom_id: str, label: Optional[str],
                 emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=style, custom_id=custom_id, label=label, emoji=emoji)

    async def callback(self, interaction: discord.Interaction):
        self.view.value = self.custom_id
        self.view.stop()


class DropTypeSelect(discord.ui.Select):
    """Drop type select"""
    def __init__(self, drop_types: List[str], active_drop_type: str, placeholder: str, row: Optional[int] = None):
        self.drop_types = drop_types
        options = []
        for drop_type in drop_types:
            label = drop_type
            emoji = '🔹' if drop_type == active_drop_type else None
            options.append(discord.SelectOption(label=label, value=label, emoji=emoji))
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options, row=row,
                         custom_id='select_type')

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_drop_type = select_value
        for child in self.view.children:
            if child.custom_id == 'select_type':
                options = []
                for drop_type in self.drop_types:
                    label = drop_type
                    emoji = '🔹' if drop_type == self.view.active_drop_type else None
                    options.append(discord.SelectOption(label=label, value=label, emoji=emoji))
                child.options = options
                break
        if 'lootbox' in self.view.active_drop_type.lower():
            boost_percentage = self.view.lootbox_boost_percentage
            world_boost = self.view.lootbox_world_boost
        else:
            boost_percentage = self.view.mob_boost_percentage
            world_boost = self.view.mob_world_boost
        embed = await self.view.embed_function(self.view.active_drop_type, self.view.timetravel, self.view.horse_data,
                                               world_boost, boost_percentage, self.view.vampire_teeth_artifact,
                                               self.view.claus_belt_artifact)
        await interaction.response.edit_message(embed=embed, view=self.view)


class TimeJumpCalculatorEnchantSelect(discord.ui.Select):
    """Enchant select"""
    def __init__(self, enchant_type: Literal['armor', 'sword'], placeholder: str, row: Optional[int] = None):
        enchants = [
            'OMEGA',
            'ULTRA-OMEGA',
            'GODLY',
            'VOID'
        ]
        options = []
        options.append(discord.SelectOption(label='None', value='None', emoji=None))
        for enchant in enchants:
            options.append(discord.SelectOption(label=enchant, value=enchant, emoji=emojis.PR_ENCHANTER))
        self.enchants = enchants
        self.enchant_type = enchant_type
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options, row=row,
                         custom_id=f'select_enchant_{enchant_type}')

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        if select_value == 'None': select_value = 'No'
        self.view.profile_data[f'enchant_{self.enchant_type}'] = select_value
        for child in self.view.children:
            if child.custom_id == self.custom_id:
                options = []
                options.append(discord.SelectOption(label='None', value='None', emoji=None))
                for enchant in self.enchants:
                    options.append(discord.SelectOption(label=enchant, value=enchant, emoji=emojis.PR_ENCHANTER))
                child.options = options
                break
        embed = await self.view.embed_function(self.view.area_no, self.view.inventory, self.view.profile_data,
                                               self.view.boosts_data, self.view.option_inventory, self.view.option_stats)
        await interaction.response.edit_message(embed=embed, view=self.view)


class TimeJumpCalculatorGearSelect(discord.ui.Select):
    """Gear select"""
    def __init__(self, gear_type: Literal['armor', 'sword'], all_items: dict, placeholder: str, profile_data: dict,
                 row: Optional[int] = None):
        options = []
        if profile_data[gear_type] is not None:
            options.append(discord.SelectOption(label='None', value='None', emoji=None))
        item_counter = 1
        for item in all_items.values():
            if item.score == 0: continue
            if item.item_type == gear_type:
                if profile_data[gear_type].name == item.name: continue
                options.append(discord.SelectOption(label=item.name, value=item.name, emoji=item.emoji))
                item_counter += 1
                if item_counter == 25: break
        self.gear_type = gear_type
        self.all_items = all_items
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options, row=row,
                         custom_id=f'select_gear_{gear_type}')

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        if select_value == 'None':
            self.view.profile_data[self.gear_type] = None
        else:
            self.view.profile_data[self.gear_type] = self.all_items[select_value]
        for child in self.view.children:
            if child.custom_id == self.custom_id:
                options = []
                if self.view.profile_data[self.gear_type] is not None:
                    options.append(discord.SelectOption(label='None', value='None', emoji=None))
                item_counter = 1
                for item in self.all_items.values():
                    if item.score == 0: continue
                    if self.view.profile_data[self.gear_type] is not None:
                        if self.view.profile_data[self.gear_type].name == item.name: continue
                    if item.item_type == self.gear_type:
                        options.append(discord.SelectOption(label=item.name, value=item.name, emoji=item.emoji))
                        item_counter += 1
                        if item_counter == 25: break
                child.options = options
                break
        embed = await self.view.embed_function(self.view.area_no, self.view.inventory, self.view.profile_data,
                                               self.view.boosts_data,
                                               self.view.option_inventory, self.view.option_stats)
        await interaction.response.edit_message(embed=embed, view=self.view)


class TimeJumpCalculatorChangeStatsButton(discord.ui.Button):
    """Button to open a modal to input stats"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=None)

    async def callback(self, interaction: discord.Interaction) -> None:
        modal = modals.TimeJumpCalculatorStatsModal(self.view)
        await interaction.response.send_modal(modal)


class PetTierSelect(discord.ui.Select):
    """Pet tier Select"""
    def __init__(self, pet_tier: int, placeholder: Optional[str] = 'Choose pet tier ...',
                 row: Optional[int] = None):
        pet_tiers = {0: 'All tiers'}
        for tier in range(1,21):
            pet_tiers[tier] = f'Tier {tier}'
        options = []
        for tier, label in pet_tiers.items():
            label = label
            emoji = '🔹' if tier == pet_tier else None
            options.append(discord.SelectOption(label=label, value=str(tier), emoji=emoji))
        self.pet_tiers = pet_tiers
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options, row=row,
                         custom_id='select_tier')

    async def callback(self, interaction: discord.Interaction):
        select_value = int(self.values[0])
        self.view.pet_tier = select_value
        for child in self.view.children:
            if child.custom_id == 'select_tier':
                options = []
                for tier, label in self.pet_tiers.items():
                    label = label
                    emoji = '🔹' if tier == self.view.pet_tier else None
                    options.append(discord.SelectOption(label=label, value=str(tier), emoji=emoji))
                child.options = options
                break
        embed = await self.view.embed_function(self.view.tt_no, self.view.pet_tier)
        await interaction.response.edit_message(embed=embed, view=self.view)


class ItemSelect(discord.ui.Select):
    """Item Select"""
    def __init__(self, items: dict, active_item: str, placeholder: str, row: Optional[int] = None):
        self.items = items
        options = []
        for item, item_data in items.items():
            label = item
            emoji = item_data[0]
            options.append(discord.SelectOption(label=label, value=label, emoji=emoji))
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options, row=row,
                         custom_id='select_item')

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_item = select_value
        embed = await self.view.items[select_value][1]()
        await interaction.response.edit_message(embed=embed, view=self.view)


class ManageUserSettingsSelect(discord.ui.Select):
    """Select to change user settings"""
    def __init__(self, view: discord.ui.View, row: Optional[int] = None):
        options = []
        label_ascended = 'Set as not ascended' if view.user_settings.ascended else 'Set as ascended'
        quick_trade_emoji = emojis.ENABLED if view.user_settings.quick_trade_enabled else emojis.DISABLED
        options.append(discord.SelectOption(label='Set current TT', emoji=None,
                                            value='set_tt'))
        options.append(discord.SelectOption(label=label_ascended, emoji=None,
                                            value='toggle_ascension'))
        options.append(discord.SelectOption(label='Quick trade calculator', emoji=quick_trade_emoji,
                                            value='toggle_quick_trade'))
        super().__init__(placeholder='Change settings', min_values=1, max_values=1, options=options, row=row,
                         custom_id='manage_user_settings')

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        if select_value == 'toggle_ascension':
            if self.view.user_settings.ascended and self.view.user_settings.tt >= 25:
                await interaction.response.send_message(
                    f'Invalid combination. You can\'t set yourself as not ascended if you are {emojis.TIME_TRAVEL} TT 25+.',
                    ephemeral=True
                )
            elif not self.view.user_settings.ascended and self.view.user_settings.tt == 0:
                await interaction.response.send_message(
                    f'Invalid combination. You can\'t ascend in {emojis.TIME_TRAVEL} TT 0.',
                    ephemeral=True
                )
            else:
                await self.view.user_settings.update(ascended=not self.view.user_settings.ascended)
        elif select_value == 'toggle_quick_trade':
            await self.view.user_settings.update(quick_trade_enabled=not self.view.user_settings.quick_trade_enabled)
        elif select_value == 'set_tt':
            modal = modals.SetCurrentTTModal(self.view)
            await interaction.response.send_modal(modal)
            return
        for child in self.view.children.copy():
            if isinstance(child, ManageUserSettingsSelect):
                self.view.remove_item(child)
                self.view.add_item(ManageUserSettingsSelect(self.view))
                break
        embed = await self.view.embed_function(self.view.ctx, self.view.user_settings)
        if interaction.response.is_done():
            await interaction.message.edit(embed=embed, view=self.view)
        else:
            await interaction.response.edit_message(embed=embed, view=self.view)