import random


# Базовые характеристики через 4d6 drop lowest
def roll_stat():
    rolls = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(rolls)[1:])  # Отбрасываем минимальный результат


RACE_BONUSES = {
    # Основные расы из Player's Handbook (PHB)
    "Human": {"all": 1},  # +1 ко всем характеристикам
    "High Elf": {"Dexterity": 2, "Intelligence": 1},
    "Wood Elf": {"Dexterity": 2, "Wisdom": 1},
    "Dark Elf (Drow)": {"Dexterity": 2, "Charisma": 1},
    "Hill Dwarf": {"Constitution": 2, "Wisdom": 1},
    "Mountain Dwarf": {"Constitution": 2, "Strength": 2},
    "Lightfoot Halfling": {"Dexterity": 2, "Charisma": 1},
    "Stout Halfling": {"Dexterity": 2, "Constitution": 1},
    "Dragonborn": {"Strength": 2, "Charisma": 1},
    "Forest Gnome": {"Intelligence": 2, "Dexterity": 1},
    "Rock Gnome": {"Intelligence": 2, "Constitution": 1},
    "Half-Elf": {"Charisma": 2, "any_two": 1},  # +2 к Charisma, +1 к двум другим
    "Half-Orc": {"Strength": 2, "Constitution": 1},
    "Tiefling": {"Charisma": 2, "Intelligence": 1},

    # Расширенные расы из Volo's Guide to Monsters (VGM)
    "Aasimar": {"Charisma": 2},
    "Firbolg": {"Wisdom": 2, "Strength": 1},
    "Goliath": {"Strength": 2, "Constitution": 1},
    "Kenku": {"Dexterity": 2, "Wisdom": 1},
    "Lizardfolk": {"Constitution": 2, "Wisdom": 1},
    "Tabaxi": {"Dexterity": 2, "Charisma": 1},
    "Triton": {"Strength": 1, "Constitution": 1, "Charisma": 1},
    "Bugbear": {"Strength": 2, "Dexterity": 1},
    "Hobgoblin": {"Constitution": 2, "Intelligence": 1},
    "Goblin": {"Dexterity": 2, "Constitution": 1},
    "Kobold": {"Dexterity": 2, "Strength": -2},  # Отрицательный бонус
    "Orc": {"Strength": 2, "Constitution": 1, "Intelligence": -2},  # Отрицательный бонус
    "Yuan-Ti Pureblood": {"Charisma": 2, "Intelligence": 1},

    # Экзотические расы из других источников
    "Aarakocra": {"Dexterity": 2, "Wisdom": 1},
    "Air Genasi": {"Constitution": 2, "Dexterity": 1},
    "Earth Genasi": {"Constitution": 2, "Strength": 1},
    "Fire Genasi": {"Constitution": 2, "Intelligence": 1},
    "Water Genasi": {"Constitution": 2, "Wisdom": 1},
    "Githyanki": {"Strength": 2, "Intelligence": 1},
    "Githzerai": {"Wisdom": 2, "Intelligence": 1},
    "Tortle": {"Strength": 2, "Wisdom": 1},
    "Changeling": {"Charisma": 2, "any_one": 1},  # +2 к Charisma, +1 к одной другой
    "Kalashtar": {"Wisdom": 2, "Charisma": 1},
    "Beasthide Shifter": {"Constitution": 1},
    "Longtooth Shifter": {"Strength": 1},
    "Swiftstride Shifter": {"Dexterity": 1},
    "Wildhunt Shifter": {"Wisdom": 1},
    "Warforged": {"Constitution": 2, "any_one": 1},  # +2 к Constitution, +1 к одной другой
    "Locathah": {"Strength": 2, "Dexterity": 1},
    "Verdan": {"Charisma": 2, "Wisdom": 1},
    "Loxodon": {"Constitution": 2, "Wisdom": 1},
    "Simic Hybrid": {"Constitution": 2, "any_one": 1},  # +2 к Constitution, +1 к одной другой
    "Vedalken": {"Intelligence": 2, "Wisdom": 1},
    "Centaur": {"Strength": 2, "Wisdom": 1},
    "Minotaur": {"Strength": 2, "Constitution": 1},
    "Leonin": {"Strength": 2, "Constitution": 1},
    "Satyr": {"Dexterity": 2, "Charisma": 1},
    "Fairy": {"Dexterity": 2, "Charisma": 1},
    "Harengon": {"Dexterity": 2, "Wisdom": 1},

    # Дополнительные расы из других источников
    "Dhampir": {"any_two": 1},  # +1 к двум характеристикам на выбор
    "Hexblood": {"any_two": 1},  # +1 к двум характеристикам на выбор
    "Reborn": {"any_two": 1},  # +1 к двум характеристикам на выбор
}


def apply_race_bonuses(stats, race):
    bonuses = RACE_BONUSES.get(race, {})

    # Обработка специальных случаев
    if "all" in bonuses:
        for stat in stats:
            stats[stat] += bonuses["all"]

    if "any_two" in bonuses:
        # Выбираем две случайные характеристики для бонуса
        chosen_stats = random.sample(list(stats.keys()), 2)
        for stat in chosen_stats:
            stats[stat] += bonuses["any_two"]

    if "any_one" in bonuses:
        # Выбираем одну случайную характеристику для бонуса
        chosen_stat = random.choice(list(stats.keys()))
        stats[chosen_stat] += bonuses["any_one"]

    # Применяем обычные бонусы
    for stat, value in bonuses.items():
        if stat in stats:
            stats[stat] += value

    # Гарантируем минимальное значение 3
    for stat in stats:
        stats[stat] = max(stats[stat], 3)

    return stats

def generate_stats(race):
    stats = {
        "Strength": roll_stat(),
        "Dexterity": roll_stat(),
        "Constitution": roll_stat(),
        "Intelligence": roll_stat(),
        "Wisdom": roll_stat(),
        "Charisma": roll_stat(),
    }

    return apply_race_bonuses(stats, race)


def generate_race():
    races = [
        # Основные расы
        "Human", "Elf", "High Elf", "Wood Elf", "Dark Elf (Drow)",
        "Dwarf", "Hill Dwarf", "Mountain Dwarf", "Halfling",
        "Lightfoot Halfling", "Stout Halfling", "Dragonborn",
        "Gnome", "Forest Gnome", "Rock Gnome", "Half-Elf",
        "Half-Orc", "Tiefling",

        # Экзотические расы
        "Aasimar", "Firbolg", "Goliath", "Kenku", "Lizardfolk",
        "Tabaxi", "Triton", "Bugbear", "Hobgoblin", "Goblin",
        "Kobold", "Orc", "Yuan-Ti Pureblood", "Aarakocra",
        "Genasi", "Air Genasi", "Earth Genasi", "Fire Genasi",
        "Water Genasi", "Githyanki", "Githzerai", "Tortle",
        "Changeling", "Kalashtar", "Shifter", "Warforged",
        "Locathah", "Verdan", "Loxodon", "Simic Hybrid",
        "Vedalken", "Centaur", "Minotaur", "Leonin", "Satyr",
        "Fairy", "Harengon"
    ]
    return random.choice(races)


def generate_class():
    classes = [
        # Базовые классы
        "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
        "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer",
        "Warlock", "Wizard",

        # Дополнительные классы
        "Artificer", "Blood Hunter", "Mystic", "Psion",
        "Alchemist", "Warlord", "Hunter", "Astronomer",
        "Magus", "Savant", "Shaman", "Rune Keeper",
        "Unquiet Soul"
    ]
    return random.choice(classes)





import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()  # Загружаем токен из .env

def generate_image(prompt: str, character_id: int, model: str = "stabilityai/stable-diffusion-2-1", max_retries: int = 50):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

    # Генерация уникального имени файла
    image_filename = f"generated_image_{character_id}.png"
    image_path = os.path.join("static", image_filename)  # Правильный путь

    retries = 0
    while retries < max_retries:
        try:
            # Отправляем запрос
            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": prompt},
            )

            # Проверяем успешность запроса
            if response.status_code == 200:
                # Сохраняем изображение
                with open(image_path, "wb") as f:
                    f.write(response.content)
                return image_filename  # Возвращаем имя файла
            else:
                print(f"Ошибка генерации: {response.text}. Попытка {retries + 1} из {max_retries}")
                retries += 1
                time.sleep(60)  # Пауза перед следующей попыткой
        except Exception as e:
            print(f"Ошибка при запросе: {e}. Попытка {retries + 1} из {max_retries}")
            retries += 1
            time.sleep(60)  # Пауза перед следующей попыткой

    # Если изображение не сгенерировалось, возвращаем заглушку
    return 'placeholder.png'

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
            "maxTokens": 250,
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
    # Генерация класса
    character_class = generate_class()
    print("Generated Class:", character_class)

    # Генерация расы
    character_race = generate_race()
    print("Generated Race:", character_race)

    # Генерация характеристик
    stats = generate_stats(character_race)
    print("Generated Stats:", stats)

    # Генерация предыстории
    background = generate_text("in english generate only background for dnd character, based on:" + str(character_race) + str(character_class) + str(stats))
    print("Generated Background:", background)




    return {
        "class": character_class,
        "race": character_race,
        "stats": stats,
        "background": background,

    }



