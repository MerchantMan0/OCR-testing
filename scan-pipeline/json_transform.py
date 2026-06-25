from collections import defaultdict

import cv2
import numpy as np

from common import all_words, block_corners, center, norm_to_px


def matched_pairs(source, target):
    by_value = defaultdict(list)
    for w in all_words(target):
        by_value[w["value"]].append(w)
    src, tgt = [], []
    for w in all_words(source):
        cands = by_value.get(w["value"])
        if not cands:
            continue
        src_c = center(w)
        match = min(cands, key=lambda c: abs(center(c)[1] - src_c[1]))
        src.append(src_c)
        tgt.append(center(match))
    return np.float32(src), np.float32(tgt)


def homography(source, target, scan_shape):
    h_out, w_out = source["dimensions"]
    src_pts, tgt_pts = matched_pairs(source, target)
    matrix, inliers = cv2.findHomography(
        norm_to_px(tgt_pts, scan_shape),
        norm_to_px(src_pts, (h_out, w_out)),
        cv2.RANSAC,
        5.0,
    )
    return matrix, inliers


def affine_norm(source, target):
    return cv2.estimateAffinePartial2D(block_corners(source), block_corners(target))


def project_affine(points, matrix):
    pts = np.asarray(points, dtype=np.float32).reshape(-1, 1, 2)
    return cv2.transform(pts, matrix).reshape(-1, 2)
