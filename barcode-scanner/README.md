# Сканер QR-кодов и штрихкодов (Code128)

Генерация и распознавание кодов, которые используются для маркировки изделий и учёта: QR и Code128. Найденные коды обводятся на изображении вместе с расшифровкой.

![Code128](docs/code128_demo_scanned.png)

## Использование

```bash
# Linux: sudo apt-get install libzbar0
python -m codescan gen-code128 "DEVICE|ECG-DEMO-01|SN-0001" out.png
python -m codescan gen-qr "DEVICE|ECG-DEMO-01|SN-0001" qr.png
python -m codescan scan out.png --annotate out_scanned.png
```

```python
from codescan import make_qr, scan_image
path = make_qr("hello", "q.png")
print([(r.kind, r.data) for r in scan_image(path)])
```

Демо: `python examples/demo.py`. Тесты: `pytest`.

## Ограничения

Читаются чёткие синтетические изображения. Работа с фотографиями (наклон, блики, размытие) в тестах не проверялась.
