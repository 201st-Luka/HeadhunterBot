from interactions import Extension, Client, extension_command, CommandContext, Option, OptionType, Embed, extension_autocomplete, Choice

from Bot.Exeptions import InvalidCommandSyntax, InvalidPlayerTag
from Bot.Extensions.Extensionssetup import extension_command_wrapper
from Bot.Methods import kwargs2clan_and_tag
from CocApi.Clans.Clan import clan
from CocApi.Players.PLayer import player
from Database.Data_base import DataBase
from Database.User import User


class LinkCommand(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="link",
        description="link a player or a clan to your account or server",
        default_scope=True,
        options=[
            Option(name="player",
                   description="link a player",
                   type=OptionType.SUB_COMMAND_GROUP,
                   options=[
                       Option(name="add",
                              description="adds a player tag for your account",
                              type=OptionType.SUB_COMMAND,
                              options=[
                                  Option(name="tag",
                                         description="enter your player tag you want to add",
                                         required=True,
                                         type=OptionType.STRING)
                              ]),
                       Option(name="remove",
                              description="removes a player tag from your account",
                              type=OptionType.SUB_COMMAND,
                              options=[
                                  Option(name="player",
                                         description="select your player you want to remove",
                                         required=True,
                                         type=OptionType.STRING,
                                         autocomplete=True)
                              ]),
                       Option(name="info",
                              description="shows all linked player tags to your account",
                              type=OptionType.SUB_COMMAND)
                   ]),
            Option(name="clan",
                   description="link a player",
                   type=OptionType.SUB_COMMAND_GROUP,
                   options=[
                       Option(name="set",
                              description="sets the clan tag for your guild",
                              type=OptionType.SUB_COMMAND,
                              options=[
                                  Option(name="tag",
                                         description="enter your clan tag you want to set",
                                         required=True,
                                         type=OptionType.STRING)
                              ]),
                       Option(name="delete",
                              description="deletes the clan tag from your guild",
                              type=OptionType.SUB_COMMAND,
                              options=[Option(name="clan",
                                              description="your linked clan",
                                              required=True,
                                              type=OptionType.STRING,
                                              autocomplete=True)
                                       ]
                              ),
                       Option(name="info",
                              description="shows the linked clan tag of your guild",
                              type=OptionType.SUB_COMMAND)
                   ])
        ]
    )
    @extension_command_wrapper
    async def link(self, ctx: CommandContext, **kwargs):
        match kwargs['sub_command_group']:
            case 'player':  # PLAYER ----------------------------------------------------
                match kwargs['sub_command']:
                    case 'add':  # add --------------------------------------------------
                        kwargs['tag'] = kwargs['tag'].strip("#")
                        player_response = player(kwargs['tag'])
                        if ctx.user.id in self.user.users.fetch_user_ids():
                            if player_response != {"reason": "notFound"}:
                                if kwargs['tag'] not in self.user.users.fetch_player_tags(ctx.user.id):
                                    self.user.users.insert_user(ctx.user.id, kwargs['tag'], player_response['name'])
                                    player_embed = Embed(
                                        title=f"Linked {player_response['name']} (#{kwargs['tag']})",
                                        description=f"Successfully linked **{player_response['name']}** (#{kwargs['tag']}) to you."
                                    )
                                    await ctx.send(embeds=player_embed)
                                    return
                                await ctx.send(f"The player tag #{kwargs['tag']} has already been linked to you!")
                                return
                            raise InvalidPlayerTag
                        if player_response != {"reason": "notFound"}:
                            self.user.users.insert_user(ctx.user.id, kwargs['tag'], player_response['name'])
                            player_embed = Embed(
                                title=f"Linked {player_response['name']} (#{kwargs['tag']})",
                                description=f"Successfully linked **{player_response['name']}** (#{kwargs['tag']}) to you."
                            )
                            await ctx.send(embeds=player_embed)
                            return
                        raise InvalidPlayerTag
                    case 'remove':  # remove --------------------------------------------
                        player_and_tag = (kwargs['player'][:len(kwargs['player']) - len(kwargs['player'].split(" ")[-1]) - 1],
                                          kwargs['player'][len(kwargs['player']) - len(kwargs['player'].split(" ")[-1]):])
                        self.user.users.delete_user_player(ctx.user.id, player_and_tag[1])
                        player_embed = Embed(
                            title=f"Removed {player_and_tag[0]} (#{player_and_tag[1]})",
                            description=f"Successfully removed **{player_and_tag[0]}** (#{player_and_tag[1]}) from you."
                        )
                        await ctx.send(embeds=player_embed)
                        return
                    case 'info':  # info ------------------------------------------------
                        if ctx.user.id in self.user.users.fetch_user_ids():
                            players = self.user.users.fetch_all_players_of_user(ctx.user.id)
                            players.sort(key=lambda p: p[0])
                            player_embed = Embed(
                                title=f"Linked players for {ctx.user.username}#{ctx.user.discriminator}",
                                description="\n".join([f"You have {'one player' if len(players) == 1 else f'{len(players)} players'} linked:",
                                                       *[''.join((' - **', p[0], '** (', p[1], ')')) for p in players]])
                            )
                            await ctx.send(embeds=player_embed)
                            return
                        await ctx.send("You don't have any players linked.")
                        return
                    case _:
                        raise InvalidCommandSyntax
            case 'clan':  # CLAN --------------------------------------------------------
                match kwargs['sub_command']:
                    case 'set':  # set --------------------------------------------------
                        if kwargs['tag'].startswith("#"):
                            kwargs['tag'] = kwargs['tag'].strip("#")
                        clan_response = clan(kwargs['tag'])
                        if clan_response == {"reason": "notFound"}:
                            await ctx.send(f"#{kwargs['tag']} is not a valid clantag!")
                            return
                        elif not self.user.guilds.fetch_clantag(ctx.guild_id) == kwargs['tag']:
                            self.user.guilds.update_clan_tag_and_name(ctx.guild_id, kwargs['tag'], clan_response['name'])
                            clan_embed = Embed(
                                title=f"Linked {kwargs['tag']}",
                                description=f"Successfully linked **{clan_response['name']}** #{kwargs['tag']} to this server"
                            )
                            clan_embed.set_thumbnail(url=clan_response['badgeUrls']['large'])
                            await ctx.send(embeds=clan_embed)
                            return
                        else:
                            await ctx.send(f"The clan #{kwargs['tag']} has already been linked to this server")
                            return
                    case 'delete':
                        clan_and_tag = kwargs2clan_and_tag(kwargs)
                        self.user.guilds.update_clan_tag_and_name(ctx.guild_id, None, None)
                        player_embed = Embed(
                            title=f"Deleted {clan_and_tag[0]} (#{clan_and_tag[1]})",
                            description=f"Successfully deleted **{clan_and_tag[0]}** (#{clan_and_tag[1]}) from this guild."
                        )
                        await ctx.send(embeds=player_embed)
                        return
                    case 'info':
                        clan_and_tag = self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)
                        if clan_and_tag != (None, None):
                            clan_embed = Embed(
                                title=f"Linked clan for {ctx.guild.name}",
                                description=f"You have **{clan_and_tag[0]}** (#{clan_and_tag[1]}) linked."
                            )
                            await ctx.send(embeds=clan_embed)
                            return
                        await ctx.send("You don't have a linked clan.")
                        return
                    case _:
                        raise InvalidCommandSyntax
            case _:
                raise InvalidCommandSyntax

    @extension_autocomplete("link", "player")
    async def player_remove_autocomplete(self, ctx: CommandContext):
        players = self.user.users.fetch_players(ctx.user.id)
        choices = [Choice(name=f"{p[0]} (#{p[1]})", value=" ".join(p)) for p in players]
        await ctx.populate(choices)
        return

    @extension_autocomplete("link", "clan")
    async def clan_delete_autocomplete(self, ctx: CommandContext):
        clan_tag_name = self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)
        if clan_tag_name == (None, None):
            choice = []
        else:
            choice = Choice(name=f"{clan_tag_name[0]} (#{clan_tag_name[1]})", value=" ".join(clan_tag_name))
        await ctx.populate(choice)
        return


def setup(client: Client):
    LinkCommand(client)
    return
