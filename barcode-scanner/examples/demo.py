"""Демо: генерирует код «карточки изделия» с вымышленными данными и читает его.
    python examples/demo.py
Результат — docs/*.png."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from codescan import annotate, make_code128, make_qr, scan_image  # noqa: E402

docs = ROOT / "docs"
docs.mkdir(exist_ok=True)

# Вымышленная запись об изделии. Реальные персональные данные в коды не кладём!
payload = "DEVICE|ECG-DEMO-01|SN-0001|2026-10"

for name, maker in (("qr_demo.png", make_qr), ("code128_demo.png", make_code128)):
    img = maker(payload, docs / name)
    found = scan_image(img)
    print(name, "->", [(r.kind, r.data) for r in found])
    annotate(img, found, docs / name.replace(".png", "_scanned.png"))
