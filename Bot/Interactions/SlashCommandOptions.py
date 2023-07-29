from interactions import SlashCommandOption, OptionType


ClanOption = SlashCommandOption(
    name="clan",
    description="linked clans and clan war opponent or search clan by name or tag (type '#')",
    type=OptionType.STRING,
    required=True,
    autocomplete=True
)
