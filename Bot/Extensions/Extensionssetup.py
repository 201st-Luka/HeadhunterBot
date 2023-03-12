import logging
import os
from interactions import CommandContext, Extension, Client, ComponentContext

from Bot.Exeptions import NoClanTagLinked, InvalidClanTag, NoPlayerTagLinked, InvalidPlayerTag, AlreadyLinkedClanTag
from Bot.Variables import path


def setup(client: Client):
    extensions = [extension.path[len(path) + 1:-3] for extension in os.scandir(f"{path}/Bot/Extensions") if extension.is_file()]
    extensions.remove("Bot/Extensions/Extensionssetup")
    [client.load(extension) for extension in [extension.replace("/", ".") for extension in extensions]]
    return


def extension_command_wrapper(command):
    async def extension_wrapper(extension: Extension, ctx: CommandContext, *args, **kwargs):
        # logging ----------------
        logging.info(f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id}) used /{command.__name__} on guild '{ctx.guild}' "
                     f"({ctx.guild_id}) in channel '{ctx.channel}' ({ctx.channel_id}).")
        try:
            # extension command --
            await command(extension, ctx, *args, **kwargs)
            return
        # exceptions -------------
        except NoClanTagLinked:
            await ctx.send("This guild doesn't have a linked clan tag. Do `/clan link set <clan tag>` first!")
            return
        except InvalidClanTag:
            await ctx.send("Your entered clan tag is not valid!")
            return
        except NoPlayerTagLinked:
            await ctx.send("You don't have a linked player tag. Do `/linkplayer <player tag>` first!")
            return
        except InvalidPlayerTag:
            await ctx.send("Your entered player tag is not valid!")
            return
        except AlreadyLinkedClanTag:
            await ctx.send("This clan has already been linked to this server")
            return
        except Exception as exception:
            await ctx.send(
                f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                f"{str(exception)}```")
            raise

    return extension_wrapper


def extension_component_wrapper(component_callback):
    async def extension_wrapper(extension: Extension, ctx: ComponentContext, *args, **kwargs):
        # logging ----------------
        logging.info(f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id}) used the component {component_callback.__name__} on"
                     f" guild '{ctx.guild}' ({ctx.guild_id}) in channel '{ctx.channel}' ({ctx.channel_id}).")
        try:
            # mother component callback
            await component_callback(extension, ctx, *args, **kwargs)
            return
        # exceptions -------------
        except InvalidClanTag:
            await ctx.send("Your entered clan tag is not valid!")
            return
        except InvalidPlayerTag:
            await ctx.send("Your entered player tag is not valid!")
            return
        except Exception as exception:
            await ctx.send(
                f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                f"{str(exception)}```")
            raise

    return extension_wrapper
