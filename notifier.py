import numpy as np
import json
from datetime import datetime
import tempfile
import re
import smtplib
import cv2
from email.message import EmailMessage
from config import EMAIL_SENDER, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD


def load_schedule() -> tuple[int, int]:
    """
    Загружает график уведомлений из конфигурационного файла.

    Функция считывает параметры времени начала и окончания, когда уведомления могут быть отправлены.

    Returns:
        tuple[int, int]: Кортеж с двумя значениями: начало (from_hour) и конец (to_hour) периода для уведомлений.
                          Значения по умолчанию: 0 и 24 (всегда доступно для отправки уведомлений).
    """
    try:
        # Чтение конфигурационного файла
        with open("config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
            # Возвращаем значение периода времени для отправки уведомлений
            return int(cfg.get("notify_from", 0)), int(cfg.get("notify_to", 24))
    except Exception:
        # Возвращаем значения по умолчанию, если произошла ошибка (не удалось считать файл)
        return 0, 24  # по умолчанию: всегда


def is_notification_time() -> bool:
    """
    Проверяет, находится ли текущее время в периоде, когда должны быть отправлены уведомления.

    Returns:
        bool: True, если текущее время находится в допустимом периоде, иначе False.
    """
    from_hour, to_hour = load_schedule()  # Загружаем расписание уведомлений
    now_hour = datetime.now().hour  # Получаем текущий час
    # Если период не перекрывается (например, ночное время), проверяем его по соответствующим часам
    if from_hour < to_hour:
        return from_hour <= now_hour < to_hour
    else:
        return now_hour >= from_hour or now_hour < to_hour


def send_email_notification(image: np.ndarray, label: str = "Объект обнаружен") -> None:
    """
    Отправляет уведомление на электронную почту с изображением объекта.

    Функция формирует и отправляет email с прикрепленным изображением объекта и его меткой.

    Args:
        image (np.ndarray): Изображение объекта, которое будет прикреплено к email.
        label (str, optional): Метка, которая будет отображаться в теме и теле письма. По умолчанию "Объект обнаружен".
    """
    # Очистка метки от символов новой строки
    clean_label = re.sub(r'[\r\n]+', ' ', str(label)).strip()

    # Создание сообщения
    msg = EmailMessage()
    msg['Subject'] = f'🚨 Обнаружено: {clean_label}'  # Тема письма
    msg['From'] = EMAIL_SENDER  # Отправитель
    msg['To'] = EMAIL_RECEIVER  # Получатель
    msg.set_content(
        # Текст письма
        f'Обнаружен объект: {label} — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )

    # Временный файл для хранения изображения
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        img_path = tmp_file.name
        cv2.imwrite(img_path, image)  # Сохраняем изображение во временный файл

        # Добавляем изображение в качестве вложения
        with open(img_path, 'rb') as img:
            msg.add_attachment(img.read(), maintype='image',
                               subtype='jpeg', filename='detected.jpg')

    try:
        # Отправка письма через SMTP сервер
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Используем защищенное соединение
            # Авторизация на SMTP сервере
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)  # Отправка письма
            # Логирование успешной отправки
            print(f"📧 Уведомление отправлено на {EMAIL_RECEIVER}")
    except Exception as e:
        # В случае ошибки при отправке уведомляем об этом в консоли
        print(f"❌ Ошибка при отправке почты: {e}")
