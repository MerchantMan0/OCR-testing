import asyncio
import io

import discord
from docscan.doc import scan

from .utils import compress_to_jpeg, get_image_attachment, to_jpeg_bytes


async def handle_docscan(message):
    attachment = await get_image_attachment(message)
    if attachment is None:
        return
    try:
        status_msg = await message.channel.send("Docscan is in progress")
        raw = await asyncio.to_thread(to_jpeg_bytes, await attachment.read())
        output_bytes = await asyncio.to_thread(scan, raw)
        buf = await asyncio.to_thread(compress_to_jpeg, output_bytes)
        await message.channel.send(file=discord.File(buf, filename="docscan.jpg"))
        await status_msg.delete()
    except Exception as e:
        await message.channel.send(f"Error: {e}")
