# Test API & UI Client

Test API & UI Client — комплексный проект автоматизации тестирования, демонстрирующий современные подходы к построению тестовых фреймворков для API (REST) и UI (Selenium, Playwright) на Python.

---

## Архитектура проекта

```text
├── api/                        # Базовый HTTP-клиент для API
├── config/                     # Глобальные настройки проекта (settings.py)
├── helpers/retry/              # Кастомный отказоустойчивый модуль повторных попыток
├── schemas/                    # JSON-схемы для валидации API-ответов
├── services/                   # Сервисный (бизнес) слой для работы с эндпоинтами
├── tests/                      # Модульные и интеграционные API-тесты
├── ui/                         # Модуль UI-тестирования
│   ├── playwright/             # Автотесты на движке Playwright
│   └── selenium/               # Автотесты на движке Selenium (разбиты по приложениям)
│       ├── apps/
│       │   ├── automation_exercise/
│       │   ├── reqres/
│       │   ├── samokat/
│       │   └── the_internet/
│       └── core/               # Ядро Selenium (базовые страницы, умные ожидания)
├── docker/                     # Инфраструктурные файлы для контейнеризации
├── docker-compose.yml          # Оркестрация контейнеров для CI/CD запуска
└── pytest.ini                  # Конфигурация запуска тест-раннера pytest
```

---

## Компоненты фреймворка

### API Layer
В проекте используется кастомный `ApiClient` (`api/client.py`), инкапсулирующий библиотеку `requests`.
* **Сервисный слой (`services/`):** Реализует бизнес-логику поверх API-клиента (`auth_service.py`, `users_service.py`). Выделяет обработку ответов и кастомные исключения в изолированные классы.
* **Кастомные повторители (`helpers/retry/`):** Декоратор для автоматического перезапуска падавших запросов при временных ошибках (5xx) с гибко настраиваемыми политиками и конфигурациями.
* **Валидация (`schemas/`):** Валидация структуры JSON-ответов на соответствие схемам.

### UI Layer (Playwright & Selenium)
Проект поддерживает параллельную работу с двумя ведущими UI-инструментами на базе паттерна **Page Object Model (POM)** и **Flows** (высокоуровневые пользовательские сценарии).

---

## Локальная установка и запуск

### 1. Подготовка окружения
```bash
# Клонирование репозитория
git clone https://github.com/maxveresh/api-client-project.git
cd api-client-project

# Создание и активация виртуального окружения
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Запуск тестов через Pytest
```bash
pytest                             # Запуск абсолютно всех тестов в проекте
pytest tests/                      # Запуск только API тестов
pytest ui/playwright/              # Запуск UI тестов на Playwright
pytest ui/selenium/                # Запуск UI тестов на Selenium
```

### 3. Таргетированный запуск приложений в Selenium
```bash
pytest ui/selenium/apps/automation_exercise/   # Тесты интернет-магазина
pytest ui/selenium/apps/the_internet/          # Тесты типовых веб-элементов
```

---

## Запуск внутри Docker (Test Runner)

Проект полностью подготовлен для запуска в изолированных контейнерах, что исключает проблемы с несовместимостью локальных браузеров или драйверов.

```bash
# Сборка окружения и запуск всех тестов в Docker-контейнере
docker-compose up --build

# Остановка контейнеров и очистка ресурсов
docker-compose down
```

---

## Allure-отчетность

В проект интегрирован фреймворк Allure для генерации подробных интерактивных отчетов с шагами (`@allure.step`) и разделением по тест-кейсам (`@allure.title`, `@allure.story`).

### 1. Установка Allure CLI

* **MacOS:** `brew install allure`
* **Linux:** 
  ```bash
  sudo apt-add-repository ppa:qameta/allure
  sudo apt-get update && sudo apt-get install allure
  ```
* **Windows:** Скачать архив с [Официального репозитория Allure2](https://github.com/allure-framework/allure2) и добавить путь к бинарнику в системную переменную `PATH`.

### 2. Сбор результатов и генерация
```bash
# Запуск тестов со сбором артефактов
pytest --alluredir=allure-results

# Локальный просмотр отчета в браузере
allure serve allure-results
```



