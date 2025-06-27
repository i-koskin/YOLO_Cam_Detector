"""
Модуль config.py

Загружает переменные окружения из .env файла и предоставляет
константы для использования в других частях проекта.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Путь к конфигурационному файлу
CONFIG_PATH = "config.json"

# Путь к .pt модели YOLO
MODEL_PATH = "yolo_weights/yolov8s.pt"

# Email-данные для отправки уведомлений
EMAIL_SENDER: str | None = os.getenv("EMAIL_SENDER")       # Адрес отправителя
EMAIL_PASSWORD: str | None = os.getenv(
    "EMAIL_PASSWORD")   # Пароль или токен приложения
EMAIL_RECEIVER: str | None = os.getenv("EMAIL_RECEIVER")   # Адрес получателя

# Настройки SMTP-сервера
SMTP_SERVER: str | None = os.getenv("SMTP_SERVER")         # Адрес SMTP сервера
# Порт SMTP (по умолчанию 587 для TLS)
SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))

# Время (сек) между отправкой уведомлений
EMAIL_THROTTLE_SECONDS = 60

# Ссылка на RTSP-поток камеры
# RTSP URL для подключения к IP-камере
RTSP_URL: str | None = os.getenv("RTSP_URL")

# Целевые классы объектов, распознаваемых моделью
TARGET_CLASSES: list[str] = [
    'person', 'bicycle', 'car',
    'motorcycle', 'bus', 'truck',
    'bird', 'cat', 'dog'
]

# Классы, относящиеся к животным
ANIMALS: list[str] = ['bird', 'cat', 'dog']

# Фиксированная палитра для классов (BGR)
CLASS_COLOR_PALETTE = {
    "person":        (0, 0, 255),       # Красный
    "bicycle":       (255, 255, 0),     # Голубой
    "car":           (0, 255, 0),       # Зеленый
    'motorcycle':    (255, 0, 255),     # Розовый
    "bus":           (0, 255, 255),     # Желтый
    "truck":         (0, 128, 255),     # Оранжевый
    "bird":          (255, 128, 0),     # Лососевый
    "cat":           (128, 0, 255),     # Фиолетовый
    "dog":           (0, 255, 128),     # Мятный
}

# Классы, по которым может происходить распознавание номеров
LICENSE_PLATE_KEYWORDS: list[str] = [
    'car', 'motorcycle', 'bus', 'truck']

# Минимальный порог уверенности для отбора объектов
CONFIDENCE_THRESHOLD = 0.5
