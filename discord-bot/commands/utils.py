import io

import discord
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

DISCORD_MAX_BYTES = 8 * 1024 * 1024  # 8 MB


def to_jpeg_bytes(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def compress_to_jpeg(png_bytes: bytes) -> io.BytesIO:
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    quality = 90
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    while buf.tell() > DISCORD_MAX_BYTES and quality > 20:
        quality -= 10
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return buf


async def get_image_attachment(message) -> discord.Attachment | None:
    attachments = message.attachments
    if not attachments and message.reference:
        ref = message.reference.resolved or await message.channel.fetch_message(message.reference.message_id)
        attachments = ref.attachments
    if not attachments:
        await message.channel.send("This command requires an image attachment.")
        return None
    return attachments[0]
