import discord
from dpydialog import DButton

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


async def show_author_info(i: discord.Interaction, _: DButton):
    """Callback handler for the 'About yourself' button - updates message with user info."""
    await i.response.edit_message(content=_info_about_author(i))


async def show_server_info(i: discord.Interaction, _: DButton):
    """Callback handler for the 'About the server' button - updates message with server info."""
    await i.response.edit_message(content=_info_about_server(i))


@bot.tree.command(name="info")
async def show_info(i: discord.Interaction):
    """
    Slash command that displays an interactive message with buttons to show user/server information.
    Creates a message with three buttons:
    - Show user information
    - Show server information
    - Close/delete the message
    """

    # Initial message shows user information
    first_message = _info_about_author(i)

    # Create view for button components
    view = discord.ui.View()

    # Add interactive buttons to the view
    view.add_item(
        DButton(
            style=discord.ButtonStyle.blurple,
            label="About yourself",
            emoji="🕺",
            action=show_author_info,
            row=0
        )
    )
    view.add_item(
        DButton(
            label="About the server",
            emoji="🌐",
            action=show_server_info,
            row=0
        )
    )
    view.add_item(
        DButton(
            label="Open Google",
            emoji="🛜",
            url="https://google.com",
            row=2
        )
    )
    view.add_item(
        DButton(
            label="Close",
            emoji="❌",
            action=lambda inter, button: inter.message.delete(),
            row=1
        )
    )
    await i.response.send_message(content=first_message, view=view)


bot.run("...")
