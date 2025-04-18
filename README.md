# 🚨 YOLO_Cam_Detector

Проект видеомониторинга с использованием детектора объектов YOLOv8. Распознаёт людей, животных и автомобильные номера в режиме реального времени, отправляет email-уведомления и сохраняет логи с изображениями.

## 🔧 Возможности

- 🎥 Подключение к камере или видеопотоку
- 📦 Обнаружение объектов (люди, животные, авто)
- 🔢 Распознавание автомобильных номеров
- 📨 Email-уведомления в заданное время
- 🧠 Настраиваемый веб-интерфейс на FastAPI
- 📁 Сохранение логов и изображений
- 🎨 Цветовая палитра по классам
- 🔄 Автоматический перезапуск при ошибках

## 📸 Примеры работы

<img src="./docs/2025-04-16_13-45-47_dog.jpg" width="420"> <img src="./docs/2025-04-16_15-07-01_car.jpg" width="420">
<img src="./docs/2025-04-16_15-35-00_motorcycle.jpg" width="400"> <img src="./docs/2025-04-16_16-55-34_bicycle.jpg" width="400">
<img src="./docs/2025-04-17_09-14-50_bird.jpg" width="400"> <img src="./docs/2025-04-17_10-10-29_truck.jpg" width="400">

## ⚙️ Установка

```bash
git clone https://github.com/i-koskin/YOLO_Cam_Detector.git
cd YOLO_Cam_Detector
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```
## 🛠️ Интерфейс конфигурации

```bash
uvicorn web_interface:app --reload --port 8000
```
<img src="./docs/web_interface.JPG" width="500">

## 🚀 Запуск

```bash
python main.py
```

## 📁 Структура

- `logs/images/` — сохранённые кадры
- `logs/YYYY-MM-DD_log.log` — журнал работы системы
- `docs/` — скриншоты работы системы
