import json

# Файлы для хранения данных
LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

def load_data(filename, default):
    """Загружает данные из JSON файла. Если файла нет, возвращает дефолт."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_data(filename, data):
    """Сохраняет данные в JSON файл с красивыми отступами."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении {filename}: {e}")

def update_leaderboard(name, score):
    """Добавляет новый результат, сортирует и оставляет топ-10."""
    data = load_data(LEADERBOARD_FILE, [])
    data.append({"name": name, "score": score})
    # Сортировка по убыванию очков
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    save_data(LEADERBOARD_FILE, data)