from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class ScanResult:
    data: str
    kind: str                       # QRCODE, CODE128, ...
    polygon: tuple[tuple[int, int], ...]


def _scan_pyzbar(img: np.ndarray) -> list[ScanResult]:
    try:
        from pyzbar.pyzbar import decode
    except (ImportError, OSError):  # pyzbar или системная libzbar недоступны
        return []
    return [ScanResult(o.data.decode("utf-8", errors="replace"), o.type,
                       tuple((p.x, p.y) for p in o.polygon)) for o in decode(img)]


def _scan_qr_opencv(img: np.ndarray) -> list[ScanResult]:
    text, pts, _ = cv2.QRCodeDetector().detectAndDecode(img)
    if not text or pts is None:
        return []
    return [ScanResult(text, "QRCODE", tuple((int(x), int(y)) for x, y in pts.reshape(-1, 2)))]


def scan_image(path: str | Path) -> list[ScanResult]:
    """Находит и расшифровывает коды на изображении.

    Сначала pyzbar (QR и линейные коды), для QR — запасной детектор OpenCV.
    """
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"Не удалось прочитать изображение: {path}")
    results = _scan_pyzbar(img)
    if not any(r.kind == "QRCODE" for r in results):
        results += _scan_qr_opencv(img)
    return results


def annotate(path: str | Path, results: list[ScanResult], out: str | Path) -> Path:
    """Рисует контуры и расшифровку поверх исходного изображения."""
    img = cv2.imread(str(path))
    pad = 35  # поле сверху, чтобы подпись не обрезалась
    img = cv2.copyMakeBorder(img, pad, 0, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    for r in results:
        pts = np.array(r.polygon, np.int32).reshape((-1, 1, 2)) + np.array([0, pad], np.int32)
        cv2.polylines(img, [pts], True, (255, 0, 0), 3)
        x, y = int(pts[:, 0, 0].min()), int(pts[:, 0, 1].min())
        cv2.putText(img, r.data[:40], (x, max(y - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 160, 0), 2)
    cv2.imwrite(str(out), img)
    return Path(out)
