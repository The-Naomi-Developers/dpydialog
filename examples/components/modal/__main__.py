import discord
from dpydialog import DModal
from dpydialog.data import ModalOption

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


async def show_modal_data(i: discord.Interaction, modal: DModal):
    """
    Callback handler for modal submission - sends a greeting message with the user's input.

    Args:
        i: The Discord interaction object
        modal: The modal containing user's input data
    """
    name: str = modal.name.value
    last_name: str = modal.last_name.value

    await i.response.send_message(
        f"Oh, hello, {name.title()} {last_name.title()}", ephemeral=True
    )


@bot.tree.command(name="info")
async def show_info(i: discord.Interaction):
    """
    Slash command that displays a modal form asking for user's name and last name.
    When submitted, responds with a greeting using the provided information.
    """
    modal = DModal(
        action=show_modal_data,
        title="I would like to know who are you!",
        options=[
            ModalOption(
                varname="last_name",
                label="Enter your last name",
                required=False,
                row=1  # will be displayed below the name field
            ),
            ModalOption(
                varname="name",
                label="Enter your name",
                placeholder="Catherine, maybe",
                row=0  # will be displayed first
            )
        ],
    )
    await i.response.send_modal(modal)


bot.run("...")
