# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    bash \
    procps \
    net-tools \
    vim \
    nano \
    htop \
    tree \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Google Cloud SDK
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz \
    && tar -xf google-cloud-cli-linux-x86_64.tar.gz \
    && ./google-cloud-sdk/install.sh --quiet \
    && rm google-cloud-cli-linux-x86_64.tar.gz

# Добавляем Google Cloud SDK в PATH
ENV PATH="/app/google-cloud-sdk/bin:${PATH}"

# Копируем исходный код приложения
COPY src/ ./src/

# Создаем директорию для базы данных
RUN mkdir -p src/database

# Устанавливаем переменные окружения
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 5000

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Команда запуска
CMD ["python", "src/main.py"]
