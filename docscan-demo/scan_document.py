import os
from pathlib import Path

os.environ.setdefault("U2NET_HOME", str(Path(__file__).parent / ".cache" / "u2net"))

from docscan.doc import scan

inp = next(Path("input").iterdir()) # find first file
out = Path("output/out.jpg") # output file location
out.write_bytes(scan(inp.read_bytes())) # transform image to flat image
