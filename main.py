import random

def roll_stat():
    rolls = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(rolls)[1:])  # Отбрасываем минимальное значение

def generate_stats():
    stats = {
        "Strength": roll_stat(),
        "Dexterity": roll_stat(),
        "Constitution": roll_stat(),
        "Intelligence": roll_stat(),
        "Wisdom": roll_stat(),
        "Charisma": roll_stat(),
    }
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







def generate_class():
    classes = ["Fighter", "Wizard", "Rogue", "Cleric", "Barbarian", "Bard", "Druid", "Paladin", "Monk", "Ranger"]
    return random.choice(classes)

def generate_background(stats, character_class):
    background_templates = [
        f"Born in a small village, your character developed {max(stats, key=stats.get)} from an early age. "
        f"After a life-changing event, they decided to become a {character_class}.",

        f"Your character grew up in a bustling city, where they honed their {max(stats, key=stats.get)}. "
        f"Seeking adventure, they chose the path of a {character_class}.",

        f"Raised in the wilderness, your character learned to rely on their {max(stats, key=stats.get)}. "
        f"Now, they travel the world as a {character_class}."
    ]
    return random.choice(background_templates)

def generate_character():
    # Генерация характеристик
    stats = generate_stats()
    print("Generated Stats:", stats)

    # Генерация класса
    character_class = generate_class()
    print("Generated Class:", character_class)

    # Генерация предыстории
    background = generate_background(stats, character_class)
    print("Generated Background:", background)

    image_path = generate_image("Create a detailed full-body image of a character facing the viewer. The character should be visualized based on their background, class. Here are the details:Background: " + background + "Class: " + character_class + "The image should be realistic, with a focus on the character's face to convey their emotions and personality. The clothing and armor should match their class and background. The background should be neutral so as not to distract from the character itself. without text. character must be all on image. character in middle ages. in fantastic world. farmat: 768x768")
    print(f"Изображение сохранено: {image_path}")

    return {
        "stats": stats,
        "class": character_class,
        "background": background,
    }

# Запуск генерации персонажа
generate_character()
