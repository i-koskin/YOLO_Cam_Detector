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

## 📸 Пример работы

<img src="./docs/web_interface.JPG" width="600">
<img src="./docs/2025-04-16_13-45-47_dog.jpg" width="600">
<img src="./docs/2025-04-16_15-07-01_car.jpg" width="600">
<img src="./docs/2025-04-16_15-35-00_motorcycle.jpg" width="600">
<img src="./docs/2025-04-16_16-55-34_bicycle.jpg" width="600">
<img src="./docs/2025-04-17_09-14-50_bird.jpg" width="600">
<img src="./docs/2025-04-17_10-10-29_truck.jpg" width="600">

## ⚙️ Установка

```bash
git clone https://github.com/i-koskin/YOLO_Cam_Detector.git
cd YOLO_Cam_Detector
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 🚀 Запуск

```bash
python main.py
```

##  🛠 Настройки

Файл `config.json`:
```json
{
  "notify_from": "07:00",
  "notify_to": "22:00",
  "notifications_enabled": true,
  "save_full_frame": true,
  "log_level": "DEBUG"
}
```

## ⚙️ Интерфейс конфигурации

```bash
uvicorn web_interface:app --reload --port 8000
```

## 📁 Структура

- `logs/images/` — сохранённые кадры
- `logs/YYYY-MM-DD_log.log` — журнал работы системы
- `docs/` — скриншоты работы системы
