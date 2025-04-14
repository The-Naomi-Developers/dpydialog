import discord
from dpydialog import DSelect

MY_GUILD = discord.Object(id=1078657744090959912)  # Replace with your server ID


class SimpleClient(discord.Client):
    """A basic Discord bot client that handles slash command registration."""

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


bot = SimpleClient()


def _info_about_author(i: discord.Interaction) -> str:
    """
    Creates a formatted string containing information about the user who triggered the interaction.
    
    Args:
        i: The Discord interaction object
    
    Returns:
        A formatted string containing user information
    """
    user = i.user

    return "\n".join(
        [
            f"**About {user.mention}**",
            f"- name: {user.name}",
            f"- id: `{user.id}`",
            f"- created at: <t:{round(user.created_at.timestamp())}:R>",
        ]
    )


def _info_about_server(i: discord.Interaction) -> str:
    """
    Creates a formatted string containing information about the server where the interaction occurred.
    
    Args:
        i: The Discord interaction object
    
    Returns:
        A formatted string containing server information
    """
    guild = i.guild

    return "\n".join(
        [
            f"**About {guild.name}**",
            f"- id: `{guild.id}`",
            f"- created at: <t:{round(guild.created_at.timestamp())}:R>",
        ]
    )


async def update_message(i: discord.Interaction, select: DSelect):
    """
    Callback function for the select menu that updates or deletes the message based on selection.
    
    Args:
        i: The Discord interaction object
        select: The DSelect component that triggered the callback
    """
    value = select.values[0]

    if value == "author":
        content = _info_about_author(i)
    if value == "server":
        content = _info_about_server(i)
    if value == "close":
        return await i.message.delete()

    await i.response.edit_message(content=content)


@bot.tree.command(name="info")
async def show_info(i: discord.Interaction):
    """
    Slash command that displays an interactive message with a select menu.
    The menu allows users to view information about themselves, the server,
    or delete the message.
    """
    first_message = _info_about_author(i)
    view = discord.ui.View()

    view.add_item(
        DSelect(
            options=[
                discord.SelectOption(
                    label="Tell me about me...", emoji="🕺", value="author"
                ),
                discord.SelectOption(
                    label="Tell me about this mysterious place...",
                    emoji="🌐",
                    value="server",
                ),
                discord.SelectOption(
                    label="Let's kill that message!", emoji="🛑", value="close"
                ),
            ],
            action=update_message,
        )
    )
    await i.response.send_message(content=first_message, view=view)


bot.run("...")
