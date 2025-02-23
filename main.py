import random

def roll_stat():
    rolls = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(rolls)[1:])  # Отбрасываем минимальное значение

def generate_stats():
    stats = {}
    used_values = set()  # Множество для отслеживания уже использованных значений

    for stat in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
        while True:
            value = roll_stat()
            if value not in used_values:  # Проверяем, не использовалось ли значение
                stats[stat] = value
                used_values.add(value)
                break

    return stats




import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем токен из .env

def generate_image(prompt: str, model: str = "stabilityai/stable-diffusion-2-1"):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

    # Отправляем запрос
    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": prompt},
    )

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Сохраняем изображение
        image_path = "generated_image.png"
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    else:
        raise Exception(f"Ошибка генерации: {response.text}")




def generate_race():
    races = ["Human", "Elf", "High Elf", "Wood Elf", "Dark Elf (Drow)", "Dwarf", "Hill Dwarf", "Mountain Dwarf", "Halfling", "Lightfoot Halfling", "Stout Halfling", "Dragonborn", "Gnome", "Forest Gnome", "Rock Gnome", "Half-Elf", "Half-Orc", "Tiefling",]
    return random.choice(races)


def generate_class():
    classes = ["Bard", "Barbarian", "Warrior", "Wizard", "Druid", "Cleric", "Artificer", "Warlock", "Monk", "Paladin", "Rogue", "Ranger", "Sorcerer", "Alchemist", "Warlord", "Hunter", "Astronomer", "Magus", "Mystic", "Savant", "Shaman", "Rune Keeper", "Unquiet Soul", "Blood Hunter"]
    return random.choice(classes)


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
            "maxTokens": 1000,
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
def generate_character():
    # Генерация характеристик
    stats = generate_stats()
    print("Generated Stats:", stats)

    # Генерация класса
    character_class = generate_class()
    print("Generated Class:", character_class)

    # Генерация расы
    character_race = generate_race()
    print("Generate race:", character_race)

    # Генерация предыстории
    background = generate_text("in english. in middle age epoch. create background for character, you have:" + str(stats) + str(character_class + str(character_race)))
    print("Generated Background:", background)

    image_path = generate_image("Create a detailed full-body image of a character facing the viewer. The character should be visualized based on their background, class, race. Here are the details:Background: " + background + "The image should be realistic, with a focus on the character's face to convey their emotions and personality. The clothing and armor should match their class and background. The background should be neutral so as not to distract from the character itself. without text. character must be all on image. character in middle ages. in fantastic world. farmat: 768x768, do not cut character")
    print(f"Изображение сохранено: {image_path}")

    return {
        "stats": stats,
        "class": character_class,
        "background": background,
        "image": image_path
    }

# Запуск генерации персонажа
generate_character()
