import numpy as np


def all_words(page):
    for block in page["blocks"]:
        for line in block["lines"]:
            yield from line["words"]


def center(word):
    (x0, y0), (x1, y1) = word["geometry"]
    return np.float32([(x0 + x1) / 2, (y0 + y1) / 2])


def norm_to_px(pts, hw):
    h, w = hw
    out = pts.copy()
    out[:, 0] *= w
    out[:, 1] *= h
    return out


def block_corners(page):
    (x0, y0), (x1, y1) = page["blocks"][0]["geometry"]
    return np.float32([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])


def zone_right_of(geometry):
    (x0, y0), (x1, y1) = geometry
    w, h = x1 - x0, y1 - y0
    return np.float32([[[x1, y0]], [[x1 + w, y1 + h]]])
