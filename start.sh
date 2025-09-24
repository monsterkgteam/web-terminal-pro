#!/bin/bash

# Скрипт для запуска Web Terminal Pro

echo "🚀 Запуск Web Terminal Pro..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверяем наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

# Создаем директорию для данных
mkdir -p data

# Проверяем переменную окружения ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  Переменная ANTHROPIC_API_KEY не установлена."
    echo "   Claude AI не будет работать без API ключа."
    echo "   Установите ключ: export ANTHROPIC_API_KEY=your_api_key"
    echo ""
fi

# Собираем и запускаем контейнер
echo "🔨 Сборка Docker образа..."
docker-compose build

echo "🚀 Запуск приложения..."
docker-compose up -d

# Ждем запуска
echo "⏳ Ожидание запуска сервиса..."
sleep 10

# Проверяем статус
if docker-compose ps | grep -q "Up"; then
    echo "✅ Web Terminal Pro успешно запущен!"
    echo ""
    echo "🌐 Откройте в браузере: http://localhost:5000"
    echo "📱 Для iPad: http://[IP-адрес]:5000"
    echo ""
    echo "📋 Полезные команды:"
    echo "   docker-compose logs -f    # Просмотр логов"
    echo "   docker-compose stop       # Остановка"
    echo "   docker-compose restart    # Перезапуск"
    echo "   docker-compose down       # Полная остановка и удаление"
    echo ""
else
    echo "❌ Ошибка запуска. Проверьте логи:"
    docker-compose logs
fi
