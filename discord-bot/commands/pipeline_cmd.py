import asyncio
import io

import discord
from docscan.doc import scan

from .doctr import doctr_lock, run_doctr
from .transform.pipeline import run_transform
from .utils import collect_attachments, compress_to_jpeg, get_image_attachment, read_json_attachment, to_jpeg_bytes


async def handle_pipeline(message):
    image = await get_image_attachment(message)
    if image is None:
        return

    attachments = await collect_attachments(message)
    source_bytes = await read_json_attachment(attachments, "source")
    if source_bytes is None:
        await message.channel.send("This command requires a `source.json` attachment.")
        return

    try:
        status_msg = await message.channel.send("Docscan in progress...")
        raw = await asyncio.to_thread(to_jpeg_bytes, await image.read())
        scanned = await asyncio.to_thread(scan, raw)
        scanned_jpeg = await asyncio.to_thread(to_jpeg_bytes, scanned)

        await status_msg.edit(content="Running doctr...")
        async with doctr_lock:
            doctr_img, ocr_json = await asyncio.to_thread(run_doctr, scanned_jpeg)

        await status_msg.edit(content="Transform in progress...")
        transformed = await asyncio.to_thread(run_transform, scanned_jpeg, source_bytes, ocr_json)

        docscan_buf = await asyncio.to_thread(compress_to_jpeg, scanned)
        doctr_buf = await asyncio.to_thread(compress_to_jpeg, doctr_img)
        transform_buf = await asyncio.to_thread(compress_to_jpeg, transformed)

        await message.channel.send(files=[
            discord.File(docscan_buf, filename="docscan.jpg"),
            discord.File(doctr_buf, filename="doctr_boxes.jpg"),
            discord.File(io.BytesIO(ocr_json), filename="RAW-OCR.json"),
            discord.File(transform_buf, filename="transformed.jpg"),
        ])
        await status_msg.delete()
    except Exception as e:
        await message.channel.send(f"Error: {e}")
