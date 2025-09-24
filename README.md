# Web Terminal Pro 🚀

Полнофункциональное веб-приложение с терминалом, интегрированное с **Claude AI** и **Google Cloud CLI**. Оптимизировано для использования на iPad и других мобильных устройствах.

![Web Terminal Pro](https://img.shields.io/badge/Web%20Terminal-Pro-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-SocketIO-red?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge)

## ✨ Возможности

### 🖥️ Веб-терминал
- **Полнофункциональный терминал** в браузере с поддержкой всех команд Linux
- **Реальное время** - мгновенный отклик через WebSocket соединение
- **Автоматическое изменение размера** под размер экрана
- **Поддержка цветов** и специальных символов

### 🤖 Интеграция с Claude AI
- **Прямое общение** с Claude AI через веб-интерфейс
- **Выбор модели** - Claude 3 Opus, Sonnet, Haiku
- **Настройка параметров** - количество токенов, температура
- **История чата** с красивым интерфейсом

### ☁️ Google Cloud CLI
- **Предустановленный gcloud CLI** со всеми компонентами
- **Быстрые команды** для частых операций
- **Управление проектами** и аутентификацией
- **API интеграция** для программного доступа

### 📱 Оптимизация для iPad
- **Адаптивный дизайн** под все размеры экранов
- **Сенсорное управление** с поддержкой жестов
- **Боковая панель** с быстрым доступом к функциям
- **Плавающие кнопки** для удобной навигации

## 🚀 Быстрый старт

### Предварительные требования

- **Docker** и **Docker Compose**
- **API ключ Claude** (опционально, для работы с AI)

### Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/your-username/web-terminal-pro.git
   cd web-terminal-pro
   ```

2. **Установите API ключ Claude (опционально):**
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

3. **Запустите приложение:**
   ```bash
   ./start.sh
   ```

4. **Откройте в браузере:**
   - Локально: http://localhost:5000
   - С iPad: http://[IP-адрес-сервера]:5000

## 🛠️ Ручная установка

### Без Docker

1. **Установите зависимости:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или venv\\Scripts\\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Установите Google Cloud SDK:**
   ```bash
   curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
   tar -xf google-cloud-cli-linux-x86_64.tar.gz
   ./google-cloud-sdk/install.sh
   export PATH=$PATH:$(pwd)/google-cloud-sdk/bin
   ```

3. **Запустите приложение:**
   ```bash
   python src/main.py
   ```

### С Docker

```bash
# Сборка образа
docker build -t web-terminal-pro .

# Запуск контейнера
docker run -p 5000:5000 -e ANTHROPIC_API_KEY=your_key web-terminal-pro
```

## 📖 Использование

### Терминал
- Откройте вкладку **"Терминал"**
- Используйте как обычный Linux терминал
- Все команды `gcloud` доступны из коробки
- Поддерживаются все стандартные утилиты Linux

### Claude AI
- Переключитесь на вкладку **"Claude AI"**
- Выберите модель в боковой панели
- Введите сообщение и нажмите Enter
- Получите ответ от Claude в реальном времени

### Google Cloud
- Используйте команды `gcloud` в терминале
- Или воспользуйтесь быстрыми командами в боковой панели:
  - Список аккаунтов: `gcloud auth list`
  - Список проектов: `gcloud projects list`
  - Конфигурация: `gcloud config list`

### Быстрые команды
В боковой панели доступны часто используемые команды:
- **Список аккаунтов GCloud** - показывает аутентифицированные аккаунты
- **Список проектов** - отображает доступные проекты
- **Конфигурация GCloud** - текущие настройки
- **Очистить терминал** - очищает экран терминала

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `ANTHROPIC_API_KEY` | API ключ для Claude AI | Не установлен |
| `FLASK_ENV` | Режим Flask (development/production) | production |
| `PORT` | Порт для запуска приложения | 5000 |

### Настройки Claude

В боковой панели можно настроить:
- **Модель**: Claude 3 Opus, Sonnet, Haiku
- **Максимальное количество токенов**: 1-4000

## 🏗️ Архитектура

```
web-terminal-app/
├── src/
│   ├── main.py              # Главный файл Flask приложения
│   ├── routes/
│   │   ├── terminal.py      # WebSocket терминал
│   │   ├── claude.py        # Интеграция с Claude AI
│   │   ├── gcloud.py        # Google Cloud CLI API
│   │   └── user.py          # Пользовательские маршруты
│   ├── models/
│   │   └── user.py          # Модели базы данных
│   ├── static/
│   │   └── index.html       # Фронтенд приложения
│   └── database/
│       └── app.db           # SQLite база данных
├── Dockerfile               # Конфигурация Docker
├── docker-compose.yml       # Docker Compose конфигурация
├── requirements.txt         # Python зависимости
├── start.sh                 # Скрипт быстрого запуска
└── README.md               # Документация
```

## 🔌 API Endpoints

### Терминал (WebSocket)
- `connect` - Подключение к терминалу
- `create_terminal` - Создание новой сессии
- `terminal_input` - Отправка команд
- `terminal_resize` - Изменение размера

### Claude AI
- `POST /api/claude/chat` - Отправка сообщения
- `GET /api/claude/models` - Список моделей
- `GET /api/claude/status` - Статус подключения

### Google Cloud
- `GET /api/gcloud/version` - Версия gcloud
- `GET /api/gcloud/auth/list` - Список аккаунтов
- `GET /api/gcloud/projects/list` - Список проектов
- `POST /api/gcloud/execute` - Выполнение команды
- `GET /api/gcloud/status` - Статус CLI

## 🎨 Технологии

### Backend
- **Flask** - веб-фреймворк
- **Flask-SocketIO** - WebSocket поддержка
- **Anthropic** - Claude AI SDK
- **Subprocess** - выполнение команд
- **SQLAlchemy** - ORM для базы данных

### Frontend
- **HTML5/CSS3/JavaScript** - основа интерфейса
- **Xterm.js** - терминальный эмулятор
- **Socket.IO** - WebSocket клиент
- **Tailwind CSS** - стилизация
- **Lucide Icons** - иконки

### DevOps
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация
- **Google Cloud SDK** - облачные инструменты

## 📱 Поддержка устройств

### Полная поддержка
- ✅ **iPad** (все модели)
- ✅ **iPhone** (адаптивный интерфейс)
- ✅ **Android планшеты**
- ✅ **Android смартфоны**
- ✅ **Настольные браузеры** (Chrome, Firefox, Safari, Edge)

### Особенности для мобильных
- **Адаптивная боковая панель** - скрывается на маленьких экранах
- **Плавающая кнопка** - быстрый доступ к меню
- **Сенсорная оптимизация** - увеличенные области нажатия
- **Автоматическое изменение размера** - подстройка под ориентацию

## 🔒 Безопасность

- **Изолированные контейнеры** - каждая сессия в отдельном процессе
- **Ограниченные права** - приложение работает от непривилегированного пользователя
- **CORS защита** - настроенная политика доступа
- **Валидация входных данных** - проверка всех пользовательских вводов

## 🚀 Развертывание

### Локальное развертывание
```bash
./start.sh
```

### Развертывание на сервере
```bash
# Клонирование на сервер
git clone https://github.com/your-username/web-terminal-pro.git
cd web-terminal-pro

# Настройка переменных окружения
export ANTHROPIC_API_KEY=your_key

# Запуск
./start.sh
```

### Развертывание в облаке

#### Google Cloud Run
```bash
# Сборка и развертывание
gcloud builds submit --tag gcr.io/PROJECT_ID/web-terminal-pro
gcloud run deploy --image gcr.io/PROJECT_ID/web-terminal-pro --platform managed
```

#### AWS ECS
```bash
# Создание задачи и сервиса ECS
aws ecs create-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster your-cluster --service-name web-terminal-pro
```

## 🤝 Участие в разработке

1. **Fork** репозитория
2. Создайте **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** изменения (`git commit -m 'Add amazing feature'`)
4. **Push** в branch (`git push origin feature/amazing-feature`)
5. Откройте **Pull Request**

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 🆘 Поддержка

### Часто задаваемые вопросы

**Q: Claude AI не работает**
A: Убедитесь, что установлена переменная окружения `ANTHROPIC_API_KEY`

**Q: Google Cloud команды недоступны**
A: Выполните `gcloud auth login` для аутентификации

**Q: Терминал не подключается**
A: Проверьте, что порт 5000 не заблокирован файрволом

### Получение помощи

- 📧 **Email**: support@example.com
- 💬 **Issues**: [GitHub Issues](https://github.com/your-username/web-terminal-pro/issues)
- 📖 **Wiki**: [Документация](https://github.com/your-username/web-terminal-pro/wiki)

## 🎯 Roadmap

### Версия 2.0
- [ ] Поддержка множественных терминальных сессий
- [ ] Интеграция с AWS CLI
- [ ] Файловый менеджер
- [ ] Темы оформления

### Версия 2.1
- [ ] Совместная работа в реальном времени
- [ ] Запись и воспроизведение сессий
- [ ] Плагины и расширения
- [ ] Мобильное приложение

---

**Сделано с ❤️ для разработчиков и DevOps инженеров**
