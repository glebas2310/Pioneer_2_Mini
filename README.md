# Pioneer_2_Mini
Примеры кодов для Pioneer 2 Mini

pt_to_rknn.ipynb - блокнот Google Colab для обучения PyTorch модели и конвертации нейросетевых весов формата .pt в формат .rknn

best_model.rknn - модель для детекции на Pioneer'е (обучена на Google Colab на плохом датасете, так что сорян)

classification.py - python файл для запуска на дроне для классификации обьектов в кадре, использующий best_model.rknn. Выводит результаты через ImageViewer на http://10.42.0.1:8889/stream

flight_and_detection.py - классификация обьектов моделью .rknn, а также взлет дрона на 0.5 метра над землей и вывод через ImageViewer на http://10.42.0.1:8889/stream
