# Примеры проектов

Три небольших проекта на Python по биомедицинской инженерии: обработка сигналов, математическое моделирование и компьютерное зрение. За основу взял учебные проекты с обучения. Код переписан из ноутбуков в оформленные пакеты с тестами.

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

## Примечание

- Все данные в репозитории **синтетические**, реальные записи пациентов не публикуются.
- Это учебные и демонстрационные проекты
- В каждом README описано, что изменено по сравнению с исходным учебным заданием

## Автор

La_resp 
