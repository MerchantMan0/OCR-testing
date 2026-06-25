import cv2


def overlay(page, image) -> bytes:
    h, w = page["dimensions"]
    vis = image.copy()
    for block in page["blocks"]:
        for line in block["lines"]:
            for word in line["words"]:
                (x0, y0), (x1, y1) = word["geometry"]
                cv2.rectangle(
                    vis,
                    (int(x0 * w), int(y0 * h)),
                    (int(x1 * w), int(y1 * h)),
                    (0, 0, 255),
                    1,
                )
    ok, buf = cv2.imencode(".jpg", vis)
    if not ok:
        raise ValueError("Failed to encode overlay image.")
    return buf.tobytes()
