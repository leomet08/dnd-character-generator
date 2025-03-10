FROM python:3.11.11-slim

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache

COPY start_service.sh generated_image.png .env *.py ./
COPY static static
COPY templates templates

EXPOSE 5000

CMD bash start_service.sh
