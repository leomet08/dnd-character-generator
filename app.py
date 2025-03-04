import os
import sqlite3
from flask import Flask, render_template
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
    # Генерация персонажа только если он ещё не был создан
    if character is None:
        character = generate_character()
        # Сохранение персонажа в базу данных
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO characters (class, race, stats, background, image)
            VALUES (?, ?, ?, ?, ?)
        ''', (character['class'], character['race'], str(character['stats']), character['background'], 'generated_image.png'))  # Только имя файла
        conn.commit()
        conn.close()
    # Передача данных в HTML-шаблон
    return render_template('index.html', character=character, timestamp=int(time()))

@app.route('/characters')
def show_characters():
    conn = get_db_connection()
    characters = conn.execute('SELECT * FROM characters').fetchall()
    conn.close()
    return render_template('characters.html', characters=characters)

if __name__ == '__main__':
    app.run(debug=True)