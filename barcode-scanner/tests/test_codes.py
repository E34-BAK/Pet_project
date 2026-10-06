import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codescan import make_code128, make_qr, scan_image  # noqa: E402

PAYLOAD = "DEVICE|ECG-DEMO-01|SN-0001"


def test_qr_roundtrip(tmp_path):
    f = make_qr(PAYLOAD, tmp_path / "q.png")
    res = scan_image(f)
    assert [r.data for r in res if r.kind == "QRCODE"] == [PAYLOAD]


def test_qr_roundtrip_opencv_fallback(tmp_path, monkeypatch):
    import codescan.decode as d
    monkeypatch.setattr(d, "_scan_pyzbar", lambda img: [])
    f = make_qr(PAYLOAD, tmp_path / "q.png")
    assert [r.data for r in scan_image(f)] == [PAYLOAD]


def test_code128_roundtrip(tmp_path):
    pytest.importorskip("pyzbar.pyzbar")
    f = make_code128(PAYLOAD, tmp_path / "c.png")
    res = scan_image(f)
    assert res and res[0].kind == "CODE128" and res[0].data == PAYLOAD


def test_code128_rejects_cyrillic(tmp_path):
    with pytest.raises(ValueError):
        make_code128("Иванов", tmp_path / "x.png")


def test_empty_data_rejected(tmp_path):
    with pytest.raises(ValueError):
        make_qr("", tmp_path / "x.png")


def test_missing_image():
    with pytest.raises(FileNotFoundError):
        scan_image("no_such_file.png")


def test_blank_image_finds_nothing(tmp_path):
    import numpy as np, cv2
    p = tmp_path / "blank.png"
    cv2.imwrite(str(p), np.full((200, 200, 3), 255, np.uint8))
    assert scan_image(p) == []
