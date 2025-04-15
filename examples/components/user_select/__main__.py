import discord
from dpydialog import DUserSelect

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


async def update_message(i: discord.Interaction, select: DUserSelect):
    """Updates the message based on user selection.

    This callback function processes the selected users from a discord user select menu
    and updates the message with formatted information about each selected user.

    Args:
        i (discord.Interaction): The Discord interaction object containing response data
        select (DUserSelect): The user select component that triggered the callback
    """
    users = select.values

    result = []

    for user in users:
        result.append(
            "\n".join(
                [
                    f"**About `@{user.name}`**",
                    f"- name: {user.name}",
                    f"- id: `{user.id}`",
                    f"- created at: <t:{round(user.created_at.timestamp())}:R>",
                ]
            )
        )

    await i.response.edit_message(content="\n\n---\n\n".join(result))


@bot.tree.command(name="info")
async def show_info(i: discord.Interaction):
    """
    Slash command that displays an interactive message with a user select menu.
    The menu allows users to view information about other users.
    """
    view = discord.ui.View()

    view.add_item(
        DUserSelect(
            action=update_message,
            max_values=5
        )
    )
    await i.response.send_message(content="Select some users", view=view)


bot.run("...")
