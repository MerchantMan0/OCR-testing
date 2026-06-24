import subprocess


async def handle_free(message):
    result = subprocess.run(["free", "-h"], capture_output=True, text=True, check=True)
    await message.channel.send(f"```\n{result.stdout}\n```")
