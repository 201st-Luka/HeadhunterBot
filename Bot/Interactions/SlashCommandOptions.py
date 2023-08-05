from interactions import SlashCommandOption, OptionType

ClanOption = SlashCommandOption(
    name="clan",
    description="linked clans and clan war opponent or search clan by name or tag (type '#')",
    type=OptionType.STRING,
    required=True,
    autocomplete=True
)

PlayerOption = SlashCommandOption(
    name="player",
    description="linked players or search player by tag",
    type=OptionType.STRING,
    required=True,
    autocomplete=True
)

MemberOption = SlashCommandOption(
    name="member",
    description="clan member",
    type=OptionType.STRING,
    required=True,
    autocomplete=True
)
