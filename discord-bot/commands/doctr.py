import asyncio
import io
import json

import discord
import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.utils.visualization import visualize_page

from .utils import compress_to_jpeg, get_image_attachment, to_jpeg_bytes

print("Preparing doctr model...")
doctr_model = ocr_predictor(pretrained=True)
doctr_lock = asyncio.Lock()
print("doctr model ready.")


def run_doctr(image_bytes: bytes) -> tuple[bytes, bytes]:
    doc = DocumentFile.from_images(image_bytes)
    result = doctr_model(doc)
    page = result.pages[0].export()

    fig = visualize_page(page, doc[0], interactive=False)
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    img_buf.seek(0)

    json_buf = io.BytesIO(json.dumps(page, indent=2).encode())
    return img_buf.read(), json_buf.read()


async def handle_doctr(message):
    attachment = await get_image_attachment(message)
    if attachment is None:
        return
    try:
        status_msg = await message.channel.send("Running doctr, please wait...")
        raw = await asyncio.to_thread(to_jpeg_bytes, await attachment.read())
        async with doctr_lock:
            img_bytes, json_bytes = await asyncio.to_thread(run_doctr, raw)
        img_buf = await asyncio.to_thread(compress_to_jpeg, img_bytes)
        await message.channel.send(files=[
            discord.File(img_buf, filename="doctr_boxes.jpg"),
            discord.File(io.BytesIO(json_bytes), filename="RAW-OCR.json"),
        ])
        await status_msg.delete()
    except Exception as e:
        await message.channel.send(f"Error: {e}")
