import discord
from dpydialog import DRoleSelect
from dpydialog.errors import NotAllowedToInteract

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


async def update_message(i: discord.Interaction, select: DRoleSelect):
    """Updates message content based on selected roles.

    This callback function processes the roles selected from a Discord role select menu
    and updates the original message with formatted information about each selected role.
    The information includes the role name, ID, color and creation timestamp.

    Args:
        i (discord.Interaction): The Discord interaction object containing response data
        select (DRoleSelect): The role select component that triggered the callback
    """
    roles = select.values

    result = []

    for role in roles:
        result.append(
            "\n".join(
                [
                    f"**About `@{role.name}`**",
                    f"- name: {role.name}",
                    f"- id: `{role.id}`",
                    f"- color: `{str(role.color)}`",
                    f"- created at: <t:{round(role.created_at.timestamp())}:R>",
                ]
            )
        )

    await i.response.edit_message(content="\n\n---\n\n".join(result))


async def not_allowed(i: discord.Interaction, err: NotAllowedToInteract):
    await i.response.send_message(
        ":x: Hey, who are you?? It's not your interaction, isn't it?"
    )


@bot.tree.command(name="info")
async def show_info(i: discord.Interaction):
    """
    Slash command that displays an interactive message with a role select menu.
    The menu allows users to view information about roles.
    """
    view = discord.ui.View()

    view.add_item(DRoleSelect(action=update_message, max_values=5))
    await i.response.send_message(content="Select some roles", view=view)


bot.run("...")
