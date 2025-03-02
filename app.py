from flask import Flask, render_template
from main import generate_character

app = Flask(__name__)

@app.route('/')
def index():
    # Генерация персонажа
    character = generate_character()
    # Передача данных в HTML-шаблон
    return render_template('index.html', character=character)

if __name__ == '__main__':
    app.run(debug=True)