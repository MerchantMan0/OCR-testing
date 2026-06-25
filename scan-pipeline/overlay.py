import cv2


FIELD_COLOR = (0, 128, 0)
FIELD_IMAGE_COLOR = (0, 0, 255)  # red in BGR


def _display_label(value: str) -> str:
    if value.startswith("field_image_"):
        return value.removeprefix("field_image_")
    if value.startswith("field_"):
        return value.removeprefix("field_")
    return value


def overlay(page, image):
    h, w = page["dimensions"]
    vis = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for block in page["blocks"]:
        for line in block["lines"]:
            for word in line["words"]:
                value = word.get("value") or ""
                if not value.startswith("field"):
                    continue
                (x0, y0), (x1, y1) = word["geometry"]
                px0, py0 = int(x0 * w), int(y0 * h)
                px1, py1 = int(x1 * w), int(y1 * h)
                color = (
                    FIELD_IMAGE_COLOR
                    if value.startswith("field_image")
                    else FIELD_COLOR
                )
                cv2.rectangle(vis, (px0, py0), (px1, py1), color, 1)
                label = _display_label(value)
                scale = max(0.25, min(0.45, (px1 - px0) / max(len(label) * 7, 1)))
                ty = max(12, py0 - 2)
                cv2.putText(
                    vis,
                    label,
                    (px0, ty),
                    font,
                    scale,
                    color,
                    1,
                    cv2.LINE_AA,
                )
    return vis
