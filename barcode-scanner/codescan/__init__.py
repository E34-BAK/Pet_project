"""Генерация и распознавание QR-кодов и штрихкодов Code128."""
from .generate import make_qr, make_code128
from .decode import scan_image, annotate, ScanResult

__all__ = ["make_qr", "make_code128", "scan_image", "annotate", "ScanResult"]
