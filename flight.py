import time
from pioneer_sdk2 import Pioneer

# Инициализация дрона
drone = Pioneer()

try:
    print("Запуск моторов...")
    drone.arm()
    
    print("Взлет...")
    drone.takeoff()
    
    # Отправка дрона на высоту 0.5 м (Z) над точкой старта (X=0, Y=0)
    drone.go_to_local_point(x=0, y=0, z=0.5, yaw=0, time=3)
    
    # Ожидание достижения заданной высоты
    while not drone.point_reached():
        time.sleep(0.1)
        
    print("Высота 0.5 м достигнута. Зависание на 5 секунд...")
    time.sleep(5)

except KeyboardInterrupt:
    print("Прерывание программы оператором...")
finally:
    print("Посадка...")
    drone.land()
    time.sleep(2)
    drone.disarm()
    drone.close_connection()