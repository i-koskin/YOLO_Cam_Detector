from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import json

from config import CONFIG_PATH

# Создаем приложение FastAPI
app = FastAPI()


def load_config():
    """
    Загружает настройки из конфигурационного файла config.json.

    Функция открывает файл, загружает его содержимое в формате JSON и возвращает
    как словарь.

    Returns:
        dict: Данные из конфигурационного файла.
    """
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(from_time, to_time, enabled, save_full_frame, log_level):
    """
    Сохраняет настройки в конфигурационный файл config.json.

    Эта функция записывает переданные параметры в конфигурационный файл. Настройки
    включают время начала и окончания уведомлений, флаг для сохранения полного кадра,
    состояние уведомлений и уровень логирования.

    Args:
        from_time (str): Время начала уведомлений в формате чч:мм.
        to_time (str): Время окончания уведомлений в формате чч:мм.
        enabled (bool): Включены ли уведомления.
        save_full_frame (bool): Сохранять ли полный кадр или только ROI.
        log_level (str): Уровень логирования ("DEBUG", "INFO", "WARNING", "ERROR").
    """
    with open(CONFIG_PATH, "w") as f:
        # Сохраняем все параметры в JSON файл с отступами
        json.dump({
            "notify_from": from_time,
            "notify_to": to_time,
            "notifications_enabled": enabled,
            "save_full_frame": save_full_frame,
            "log_level": log_level  # Сохраняем выбранный уровень логирования
        }, f, indent=2, ensure_ascii=False)


@app.get("/", response_class=HTMLResponse)
def read_form():
    """
    Отображает HTML-форму для настройки уведомлений и уровня логирования.

    Эта функция генерирует HTML-страницу, на которой пользователи могут настроить:
    - Включение/выключение уведомлений.
    - Время, в течение которого уведомления будут активны.
    - Сохранение полного кадра или только ROI.
    - Уровень логирования.

    Returns:
        str: HTML-код страницы для настройки.
    """
    cfg = load_config()  # Загружаем текущие настройки из конфигурации
    # Определяем состояния чекбоксов и текущий уровень логирования
    notify_checked = "checked" if cfg.get(
        "notifications_enabled", True) else ""
    frame_checked = "checked" if cfg.get("save_full_frame", False) else ""
    # Получаем текущий уровень логирования
    log_level = cfg.get("log_level", "INFO")

    # Генерируем HTML-код для формы
    html = f"""
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        max-width: 505px;
        margin: 40px auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 8px;
        background-color: #f9f9f9;
      }}
      input[type="submit"] {{
        padding: 8px 16px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }}
      input[type="submit"]:hover {{
        background-color: #45a049;
      }}
    </style>
  </head>
  <body>
    <h2>🕒 Настройки уведомлений и сохранения</h2>
    <form method="post">
      <label>
        <input type="checkbox" name="enabled" {notify_checked}>
        Уведомления включены
      </label><br><br>

      С какого времени (чч:мм): <input name="from_time" value="{cfg.get('notify_from', '22:00')}" type="time"><br>
      До какого времени (чч:мм): <input name="to_time" value="{cfg.get('notify_to', '06:00')}" type="time"><br><br>

      <label>
        <input type="checkbox" name="save_full_frame" {frame_checked}>
        Сохранять полный кадр (а не только ROI)
      </label><br><br>

      <label>Уровень логирования:</label>
      <select name="log_level">
        <option value="DEBUG" {'selected' if log_level == 'DEBUG' else ''}>DEBUG</option>
        <option value="INFO" {'selected' if log_level == 'INFO' else ''}>INFO</option>
        <option value="WARNING" {'selected' if log_level == 'WARNING' else ''}>WARNING</option>
        <option value="ERROR" {'selected' if log_level == 'ERROR' else ''}>ERROR</option>
      </select><br><br>

      <input type="submit" value="Сохранить">
    </form>
  </body>
</html>
"""
    return html


@app.post("/")
def update_config(
    from_time: str = Form(...),
    to_time: str = Form(...),
    enabled: str = Form(None),
    save_full_frame: str = Form(None),
    log_level: str = Form(...)  # Получаем выбранный уровень логирования
):
    """
    Обновляет настройки конфигурации, включая уровень логирования.

    Эта функция получает данные из формы, обновляет конфигурационный файл и 
    перенаправляет пользователя обратно на страницу настроек.

    Args:
        from_time (str): Время начала уведомлений в формате чч:мм.
        to_time (str): Время окончания уведомлений в формате чч:мм.
        enabled (str): Строка, указывающая включены ли уведомления.
        save_full_frame (str): Строка, указывающая, сохранять ли полный кадр.
        log_level (str): Уровень логирования, выбранный пользователем.

    Returns:
        RedirectResponse: Перенаправление на страницу настроек.
    """
    # Преобразуем строки в логические значения
    notifications_enabled = enabled is not None
    save_full_flag = save_full_frame is not None
    # Сохраняем новые настройки
    save_config(from_time, to_time, notifications_enabled,
                save_full_flag, log_level)
    # Перенаправляем пользователя на страницу настроек
    return RedirectResponse("/", status_code=303)
