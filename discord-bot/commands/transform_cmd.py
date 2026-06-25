import asyncio

import discord

from .transform.pipeline import run_transform
from .utils import collect_attachments, compress_to_jpeg, read_json_attachment, to_jpeg_bytes


async def handle_transform(message):
    attachments = await collect_attachments(message)
    image = next(
        (a for a in attachments if a.content_type and a.content_type.startswith("image/")),
        None,
    )
    source_bytes = await read_json_attachment(attachments, "source")
    target_bytes = await read_json_attachment(attachments, "raw-ocr")

    if image is None or source_bytes is None or target_bytes is None:
        await message.channel.send(
            "This command requires a scan image, `source.json`, and `RAW-OCR.json`. "
            "Attach them to this message or reply to a message that includes the scan and OCR output."
        )
        return

    try:
        status_msg = await message.channel.send("Transform in progress...")
        scan_bytes = await asyncio.to_thread(to_jpeg_bytes, await image.read())
        output_bytes = await asyncio.to_thread(run_transform, scan_bytes, source_bytes, target_bytes)
        buf = await asyncio.to_thread(compress_to_jpeg, output_bytes)
        await message.channel.send(file=discord.File(buf, filename="transformed.jpg"))
        await status_msg.delete()
    except Exception as e:
        await message.channel.send(f"Error: {e}")
