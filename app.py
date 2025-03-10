import json
import os
import sqlite3
from flask import Flask, render_template, redirect, url_for
from main import generate_character, generate_image
from time import time

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect(os.environ.get("DB_PATH", "characters.db"))
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблицы, если её нет
def init_db():
    conn = get_db_connection()

    # Удаляем существующую таблицу characters, если она есть
    conn.execute('DROP TABLE IF EXISTS characters')

    # Создаём таблицу characters с правильной схемой
    conn.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class TEXT NOT NULL,
            race TEXT NOT NULL,
            background TEXT NOT NULL,
            image TEXT NOT NULL,
            stats TEXT NOT NULL  
        )
    ''')

    # Удаляем существующую таблицу character_stats, если она есть
    conn.execute('DROP TABLE IF EXISTS character_stats')

    # Создаём таблицу character_stats
    conn.execute('''
        CREATE TABLE IF NOT EXISTS character_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER NOT NULL,
            stat_name TEXT NOT NULL,
            stat_value INTEGER NOT NULL,
            FOREIGN KEY (character_id) REFERENCES characters (id)
        )
    ''')

    # Создаём индекс для ускорения поиска по character_id
    conn.execute('CREATE INDEX IF NOT EXISTS idx_character_stats_character_id ON character_stats (character_id)')

    conn.commit()
    conn.close()

# Инициализация базы данных при запуске
init_db()

# Глобальная переменная для хранения персонажа
character = None
# Функция для исправления формата stats в базе данных
def fix_stats_format():
    conn = get_db_connection()
    characters = conn.execute('SELECT * FROM characters').fetchall()

    for character in characters:
        stats = character['stats']
        try:
            # Попробуем преобразовать строку в словарь
            stats_dict = eval(stats)  # Осторожно: eval может быть опасным!
            # Преобразуем словарь в JSON
            stats_json = json.dumps(stats_dict)
            # Обновляем запись в базе данных
            conn.execute('''
                UPDATE characters SET stats = ? WHERE id = ?
            ''', (stats_json, character['id']))
        except Exception as e:
            print(f"Ошибка при обработке записи {character['id']}: {e}")

    conn.commit()
    conn.close()

# Вызов функции для исправления данных (запустите один раз, затем закомментируйте)
fix_stats_format()
@app.route('/')
def index():
    global character, image_filename
    if character is None:
        character = generate_character()
        conn = get_db_connection()

        # Сохраняем персонажа с временным изображением
        cursor = conn.execute('''
            INSERT INTO characters (class, race, background, image, stats)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            character['class'],
            character['race'],
            character['background'],
            'placeholder.png',  # Временное значение
            json.dumps(character['stats'])  # Преобразуем stats в JSON
        ))
        character_id = cursor.lastrowid

        # Генерируем уникальное изображение
        image_filename = generate_image(
            prompt=character['background'],
            character_id=character_id
        )

        # Обновляем запись с реальным именем изображения
        conn.execute('''
            UPDATE characters SET image = ? WHERE id = ?
        ''', (image_filename, character_id))

        # Сохраняем характеристики
        for stat, value in character['stats'].items():
            conn.execute('''
                INSERT INTO character_stats (character_id, stat_name, stat_value)
                VALUES (?, ?, ?)
            ''', (character_id, stat, value))

        conn.commit()
        conn.close()

    # Получаем актуальные данные из базы данных
    conn = get_db_connection()
    character_db = conn.execute('SELECT * FROM characters WHERE id = (SELECT MAX(id) FROM characters)').fetchone()
    conn.close()

    if character_db:
        character = dict(character_db)
        character['stats'] = json.loads(character['stats'])
        return render_template('index.html', character=character, timestamp=int(time()))
    else:
        return "Character not found", 404

@app.route('/generate')
def generate_new_character():
    global character
    character = generate_character()
    conn = get_db_connection()

    # Сохраняем персонажа с временным изображением
    cursor = conn.execute('''
                INSERT INTO characters (class, race, background, image, stats)
                VALUES (?, ?, ?, ?, ?)
            ''', (
        character['class'],
        character['race'],
        character['background'],
        'placeholder.png',  # Временное значение
        json.dumps(character['stats'])  # Преобразуем stats в JSON
    ))
    character_id = cursor.lastrowid

    # Генерируем уникальное изображение
    image_filename = generate_image(
        prompt=character['background'],
        character_id=character_id
    )

    # Обновляем запись с реальным именем изображения
    conn.execute('''
                UPDATE characters SET image = ? WHERE id = ?
            ''', (image_filename, character_id))

    # Сохраняем характеристики
    for stat, value in character['stats'].items():
        conn.execute('''
                    INSERT INTO character_stats (character_id, stat_name, stat_value)
                    VALUES (?, ?, ?)
                ''', (character_id, stat, value))

    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/characters')
def show_characters():
    try:
        conn = get_db_connection()
        characters = conn.execute('SELECT * FROM characters').fetchall()
        conn.close()

        characters_list = []
        for character in characters:
            try:
                stats = json.loads(character['stats'])
            except json.JSONDecodeError:
                stats = {}  # Если stats невалидный, используем пустой словарь

            characters_list.append({
                **dict(character),
                'stats': stats
            })

        return render_template('characters.html', characters=characters_list)
    except sqlite3.Error as e:
        return f"Ошибка базы данных: {e}", 500

if __name__ == '__main__':
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=os.environ.get("FLASK_PORT", "5000"),
        debug=True
    )