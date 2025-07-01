import cv2
import time
import json
import logging

from camera_stream import get_camera_stream
from detector import ObjectDetector, get_class_color
from license_plate_recognizer import PlateRecognizer
from logger import log_detection
from log_config import setup_logging
from notifier import send_email_notification, is_notification_time
from config import MODEL_PATH, EMAIL_THROTTLE_SECONDS, TARGET_CLASSES, ANIMALS, LICENSE_PLATE_KEYWORDS, CONFIDENCE_THRESHOLD

# Чтение конфигурационного файла
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

save_full_frame = cfg.get("save_full_frame", False)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Запуск логирования
setup_logging()

logger = logging.getLogger(__name__)
logger.info("🚀 Приложение запущено")


def main():
    last_email_time = 0
    cap = get_camera_stream()
    detector = ObjectDetector(MODEL_PATH)
    plate_reader = PlateRecognizer()

    cv2.namedWindow("YOLOv8 Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("YOLOv8 Detection",
                          cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    logging.info("Система запущена")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logging.warning("🔁 Повторное подключение к потоку...")
            time.sleep(1)
            cap.release()
            cap = get_camera_stream()
            continue

        frame, detections = detector.detect(frame, device)
        alert_triggered = False
        alert_label = ""
        alert_roi = None

        for det in detections:
            x1, y1, x2, y2 = det['roi']
            label = det['label']
            conf = det['conf']
            roi = frame[y1:y2, x1:x2]

            color = get_class_color(label)

            should_alert = False
            display_text = ""

            if conf < CONFIDENCE_THRESHOLD:
                continue

            if any(k in label.lower() for k in LICENSE_PLATE_KEYWORDS):
                plate = plate_reader.recognize(roi)
                display_text = f"{label} [{plate}]"
                if plate:
                    should_alert = True
                    label += f" {plate}"
            else:
                display_text = f"{label} [{conf:.2f}]"
                should_alert = True
                label += f" {conf:.2f}"

            if label:
                log_detection(frame, label, roi, save_full_frame)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            if should_alert and not alert_triggered:
                alert_triggered = True
                alert_label = display_text
                alert_roi = frame if save_full_frame else roi

        if is_notification_time():
            if alert_triggered and time.time() - last_email_time > EMAIL_THROTTLE_SECONDS:
                send_email_notification(alert_roi, alert_label)
                last_email_time = time.time()
                logging.info(f"📧 Отправлено уведомление: {alert_label}")

        cv2.imshow("YOLOv8 Detection", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in [ord('q'), 27]:  # Остановка по клавишам "q" или "Esc"
            logging.info("🛠️ Принудительная остановка пользователем")
            break

    cap.release()
    cv2.destroyAllWindows()
    logging.info("🛑 Захват остановлен")


if __name__ == "__main__":
    while True:
        try:
            main()
            logging.info("Система запущена")
        except KeyboardInterrupt:
            logging.info("Завершение по Ctrl+C")
            break
        except Exception as e:
            logging.exception(
                "❌ Критическая ошибка! Перезапуск через 5 сек...")
            time.sleep(5)
