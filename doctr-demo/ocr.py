from pathlib import Path

import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.utils.visualization import visualize_page

model = ocr_predictor(pretrained=True)

img_path = next(Path("input").iterdir())
doc = DocumentFile.from_images(img_path)
result = model(doc)

Path("output").mkdir(exist_ok=True)
fig = visualize_page(result.pages[0].export(), doc[0], interactive=False)
fig.savefig(f"output/{img_path.stem}_boxes.png", bbox_inches="tight", dpi=150)
plt.close(fig)
