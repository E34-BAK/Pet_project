from __future__ import annotations

from pathlib import Path


def make_qr(data: str, path: str | Path, box_size: int = 10, border: int = 4) -> Path:
    """Сохраняет QR-код с данными `data` в PNG."""
    import qrcode

    if not data:
        raise ValueError("data не должна быть пустой")
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    path = Path(path)
    qr.make_image(fill_color="black", back_color="white").save(path)
    return path


def make_code128(data: str, path: str | Path, quiet_zone: float = 6.0,
                 module_height: float = 15.0) -> Path:
    """Сохраняет штрихкод Code128 в PNG.

    Code128 кодирует только ASCII — кириллицу нужно транслитерировать заранее.
    quiet_zone — свободные поля по бокам; без них код часто не читается.
    """
    import barcode
    from barcode.writer import ImageWriter

    if not data:
        raise ValueError("data не должна быть пустой")
    if not data.isascii():
        raise ValueError("Code128 поддерживает только ASCII-символы")
    code = barcode.get("code128", data, writer=ImageWriter())
    stem = str(Path(path).with_suffix(""))
    saved = code.save(stem, options={"quiet_zone": quiet_zone, "module_height": module_height,
                                     "font_size": 10, "text_distance": 5.0})
    return Path(saved)
