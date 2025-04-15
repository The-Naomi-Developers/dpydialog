import asyncio
from typing import List
import discord
from dpydialog import (
    DButton,
    DRoleSelect,
    DUserSelect,
    Dialog,
    Stage,
    StageAction,
)
from dpydialog.errors import DialogException

MY_GUILD = discord.Object(id=1078657744090959912)  # Replace with your server ID


class SimpleClient(discord.Client):
    """A basic Discord bot client that handles slash command registration."""

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        # await self.tree.sync(guild=MY_GUILD)


bot = SimpleClient()


async def show_results(i: discord.Interaction, result: dict):
    # the `user` key is used because it was set in the Stage-class with keyname="user"
    users: List[discord.Member] = result.get("user")

    # same as with the `user`
    roles: List[discord.Role] = result.get("roles")

    await i.response.edit_message(
        content="Okay, the roles are being given. Wait a second...", view=None
    )

    for user in users:
        await user.add_roles(*roles, reason="The Holy Dialog has arrived.")
        await asyncio.sleep(0.5)

    await i.edit_original_response(content="The roles have been given.")


async def show_error(i: discord.Interaction, err: DialogException):
    await i.response.send_message(f"An error occured: {err}")


@bot.tree.command(name="add-roles")
async def add_role(i: discord.Interaction):
    # Since the "from_legacy_ctx" method isn't ready to use yet, you should
    #   use the "from_interaction" method with an interaction adapter for
    #   your commands.Context if you want to use the Dialog with legacy commands.
    dialog = Dialog.from_interaction(i)

    dialog.set_success_callback(show_results)
    dialog.set_error_callback(show_error)

    dialog.add_stage(
        Stage(
            keyname="user",
            components=[
                DButton(emoji="❌", row=1, action=StageAction.CLOSE),
                DButton(label="Select a user to continue", row=1, disabled=True),
                DUserSelect(
                    max_values=3,
                    row=0,
                    default_values=[i.user],
                    action=StageAction.NEXT,
                ),
            ],
        )
    ).add_stage(  # Chaining is possible
        Stage(
            keyname="roles",
            components=[
                DButton(
                    emoji="⬅️",
                    row=1,
                    style=discord.ButtonStyle.red,
                    label="Select another users",
                    action=StageAction.BACK,
                ),
                DButton(emoji="❌", row=1, action=StageAction.CLOSE),
                DRoleSelect(max_values=3, row=0, action=StageAction.NEXT),
            ],
        )
    )

    await dialog.send()


bot.run("...")
