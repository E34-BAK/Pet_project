# Biomedical Python Portfolio

Три небольших проекта на Python по биомедицинской инженерии: обработка сигналов, математическое моделирование и компьютерное зрение. Выросли из учебных работ по специальности 12.03.04 «Биотехнические системы и технологии» (МИРЭА — РТУ). Код переписан из ноутбуков в оформленные пакеты с тестами.

*English: three small Python projects (HRV autocorrelation analysis, SIR / population growth modelling, QR & Code128 scanning) refactored from university notebooks into tested packages.*

| Проект | О чём | Стек |
|---|---|---|
| [`hrv-autocorrelation`](hrv-autocorrelation) | Автокорреляционный анализ RR-интервалов: показатели C1 и C0, динамика по часам суток | NumPy, Pandas, Matplotlib |
| [`epidemic-models`](epidemic-models) | Эпидемическая модель SIR (карантин, калибровка по данным), модели роста Мальтуса и Ферхюльста | SciPy, NumPy, Matplotlib |
| [`barcode-scanner`](barcode-scanner) | Генерация и распознавание QR и Code128, разметка найденных кодов на изображении | OpenCV, pyzbar, qrcode |

## Запуск

```bash
git clone https://github.com/E34-BAK/Pet_project.git
cd Pet_project
pip install -r requirements.txt
# для barcode-scanner в Linux: sudo apt-get install libzbar0
pytest                       # все тесты
python hrv-autocorrelation/examples/demo.py
```

## Важно

- Все данные в репозитории **синтетические**. Реальные записи пациентов не публикуются.
- Это учебные и демонстрационные проекты, а не медицинские изделия. Пороги интерпретации C1 учебные, для диагностики не предназначены.
- В каждом README описано, что изменено по сравнению с исходным учебным ноутбуком.

## Автор

Мартынов Денис Русланович · студент 4 курса МИРЭА — РТУ · Telegram: @la_resp
