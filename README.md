# Pioneer_2_Mini
ПРИМЕРЫ КОДОВ ДЛЯ Pioneer 2 Mini

· pt_to_rknn.ipynb - блокнот Google Colab для обучения PyTorch модели и конвертации нейросетевых весов формата .pt в формат .rknn

· best_model.rknn - модель для детекции на Pioneer'е (обучена на Google Colab на плохом датасете, так что сорян)

· classification.py - python файл для запуска на дроне для классификации обьектов в кадре, использующий best_model.rknn. Выводит результаты через ImageViewer на http://10.42.0.1:8889/stream

· flight.py - взлет дрона на 0.5 метра

ПОДГОТОВКА К ВЗЛЕТУ:
1. Запустить дрон и дождаться полного включения

2. Нажать на кнопку быстро и коротко 3 раза (синий светодиод начнет дважды мигать)
   
3. Включить контроллер и нажать сзади кнопку BIND
 
4. Подключение по SSH, venv activate, python3 flight.py
   
ИНСТРУМЕНТЫ

· Wi-Fi: 'PMINI2...'   Password: geoscan123

· SSH: ssh pioneermini@10.42.0.1    Password: geoscan123

· SCP: scp C:/Users/AI/Downloads/file.py pioneermini@10.42.0.1:/home/pioneermini/workspace/

· InterFace: .9999

· ImageViewer: .8889/stream

· Commands: cd ls rm mkdir nano python3 source venv/bin/activate

. Sources: https://docs-beta.geoscan.ru/pioneer/ ; https://docs-beta.geoscan.ru/pioneer/ ; https://gitflic.ru/project/geoscan-llc/pioneer-rknn-example ; https://gitflic.ru/project/pioneer-team/pioneer-sdk2-example
