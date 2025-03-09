import json
import os
import sqlite3
from flask import Flask, render_template, redirect, url_for
from main import generate_character
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
    conn.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class TEXT NOT NULL,
            race TEXT NOT NULL,
            stats TEXT NOT NULL,
            background TEXT NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Инициализация базы данных при запуске
init_db()

# Глобальная переменная для хранения персонажа
character = None

@app.route('/')
def index():
    global character
    if character is None:
        character = generate_character()
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO characters (class, race, stats, background, image)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            character['class'],
            character['race'],
            json.dumps(character['stats']),  # Преобразуем словарь в JSON
            character['background'],
            'generated_image.png'
        ))
        conn.commit()
        conn.close()
    return render_template('index.html', character=character, timestamp=int(time()))

@app.route('/generate')
def generate_new_character():
    global character
    character = generate_character()
    # Сохранение персонажа в базу данных
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO characters (class, race, stats, background, image)
        VALUES (?, ?, ?, ?, ?)
    ''', (character['class'], character['race'], str(character['stats']), character['background'], 'generated_image.png'))  # Только имя файла
    conn.commit()
    conn.close()
    return redirect(url_for('index'))



@app.route('/characters')
def show_characters():
    conn = get_db_connection()
    characters = conn.execute('SELECT * FROM characters').fetchall()
    conn.close()

    # Преобразуем строку stats обратно в словарь
    characters = [
        {
            **dict(character),
            'stats': json.loads(character['stats'])  # Преобразуем строку JSON в словарь
        }
        for character in characters
    ]

    return render_template('characters.html', characters=characters)

if __name__ == '__main__':
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=os.environ.get("FLASK_PORT", "5000"),
        debug=True
    )