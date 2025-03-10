import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем API-ключ и Folder ID
API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

def generate_text(prompt: str) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "x-folder-id": FOLDER_ID,
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.9,
            "maxTokens": 2000,
        },
        "messages": [
            {
                "role": "user",
                "text": prompt,
            }
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["result"]["alternatives"][0]["message"]["text"]
    else:
        raise Exception(f"Ошибка генерации: {response.text}")

# Пример использования
prompt = """
Создай предысторию для персонажа Dungeons & Dragons.
- Класс: Варвар
- Имя: Громовержец
- Характеристики: 
  * Сила: 18
  * Ловкость: 12
  * Телосложение: 16
  * Интеллект: 8
  * Мудрость: 10
  * Харизма: 14
- Детали: 
  * Вырос в диких землях
  * Защищал племя от врагов
  * Носит топор из кости древнего дракона
  * Имеет шрамы от битв с троллями
"""


print(generate_text(prompt))
