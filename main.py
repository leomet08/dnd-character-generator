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


    return {
        "stats": stats,
        "class": character_class,
        "background": background,
    }

# Запуск генерации персонажа
character = generate_character()
print(character)