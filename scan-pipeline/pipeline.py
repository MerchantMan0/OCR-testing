import asyncio
import os
from pathlib import Path

import cv2
import numpy as np
from docscan.doc import scan
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

from image_transform import warp_to_source
from overlay import overlay

HERE = Path(__file__).parent
os.environ.setdefault("U2NET_HOME", str(HERE / ".cache" / "u2net"))

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = ocr_predictor(pretrained=True)
    return _model


def _ocr_page(model, image_bytes: bytes) -> dict:
    doc = DocumentFile.from_images(image_bytes)
    return model(doc).pages[0].export()


async def process_document(
    source: dict,
    raw_bytes: bytes,
) -> tuple[np.ndarray, np.ndarray]:
    scan_bytes = await asyncio.to_thread(scan, raw_bytes)
    scan_img = cv2.imdecode(np.frombuffer(scan_bytes, np.uint8), cv2.IMREAD_COLOR)

    model = await asyncio.to_thread(_get_model)
    target = await asyncio.to_thread(_ocr_page, model, scan_bytes)

    flat = warp_to_source(scan_img, source, target)
    return flat, overlay(source, flat)
