import json

import cv2
import numpy as np

from .image_transform import warp_to_source
from .overlay import overlay


def run_transform(scan_bytes: bytes, source_bytes: bytes, target_bytes: bytes) -> bytes:
    source = json.loads(source_bytes)
    target = json.loads(target_bytes)
    scan = cv2.imdecode(np.frombuffer(scan_bytes, np.uint8), cv2.IMREAD_COLOR)
    if scan is None:
        raise ValueError("Could not decode scan image.")
    flat = warp_to_source(scan, source, target)
    return overlay(source, flat)
