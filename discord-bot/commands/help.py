async def handle_help(message):
    from commands import COMMANDS

    command_list = "\n".join(f"`{cmd}`" for cmd in COMMANDS)
    await message.channel.send(f"**Commands:**\n{command_list}")
