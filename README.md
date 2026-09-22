# Pioneer_2_Mini
Примеры кодов для Pioneer 2 Mini

pt_to_rknn.ipynb - блокнот Google Colab для обучения PyTorch модели и конвертации нейросетевых весов формата .pt в формат .rknn

best_model.rknn - модель для детекции на Pioneer'е (обучена на Google Colab на плохом датасете, так что сорян)

classification.py - python файл для запуска на дроне для классификации обьектов в кадре, использующий модель best_model.rknn. Выводит результаты через ImageViewer на http://10.42.0.1:8889
