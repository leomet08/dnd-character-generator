FROM python:3.11.11-slim

WORKDIR /usr/src/app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения (без .env)
COPY start_service.sh generated_image.png *.py ./
COPY static static
COPY templates templates

# Создаём папку static (если её нет)
RUN mkdir -p static

EXPOSE 5000

CMD ["bash", "start_service.sh"]