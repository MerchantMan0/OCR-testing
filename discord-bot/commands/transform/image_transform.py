import cv2

from .json_transform import homography


def warp_to_source(scan, source, target):
    h_out, w_out = source["dimensions"]
    matrix, _ = homography(source, target, scan.shape[:2])
    return cv2.warpPerspective(
        scan, matrix, (w_out, h_out),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255),
    )
