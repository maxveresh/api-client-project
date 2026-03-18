# Test API Client

Test Api Client — учебный проект для практики API-автотестирования на Python.
Проект демонстрирует работу с HTTP, retry-механизмами, сервисным слоем и бизнес-ошибками.

## API
В проекте используется собственный ApiClient (api/client.py),
который инкапсулирует работу с библиотекой requests и отвечает за:

- отправку HTTP-запросов (GET, POST, PUT, PATCH, DELETE)
- логирование запросов и ответов
- единый интерфейс для сервисов

## Helpers
Retry:
    Реализует повторные попытки выполнения запросов при временных ошибках:
    - Retry при ошибках 5xx
    - Настраиваемые политики (retry_policy.py)
    - Конфигурации (retry_configs.py)
    - Универсальный декоратор (retry.py)

## Schemas
Содержит JSON-схемы для валидации ответов API. Используется в тестах для проверки структуры ответа.

## Services
Реализует бизнес-логику поверх API-клиента:

- auth_service.py — работа с авторизацией
- users_service.py — операции с пользователями
- response_handlers.py — обработка ответов
- errors.py — кастомные исключения

## Tests
API тесты с использованием pytest, фикстур, параметризацией, мокирования, покрывающие:

- API client (test_request_methods.py)
- retry механизм (test_retry_works.py)
- response handlers (test_response_handlers.py)
- сервисы (test_auth_service.py, test_users_service.py)
- интеграционные сценарии (test_login_cases.py)
- работу с внешним API (reqres)

## UI
Отдельный модуль UI-тестирования с помощью наборов инструментов Selenium Web Driver и Playwright.

### Playwright
    - Page Object Model
    - Flows (сценарии)
    - UI тесты:
          - логин
          - пользовательские сценарии

### Selenium
    - Page Object Model
    - Flows (сценарии)
    - UI тесты:
          - логин
          - пользовательские сценарии

---------------------------------------------------------------------------------------------------

# УСТАНОВКА И ЗАПУСК
1. Клонирование репозитория
    git clone https://github.com/maxveresh/api-client-project.git
    cd api-client-project
2. Создание виртуального окружения 
    python -m venv venv
3. Активация:
    source venv/bin/activate
4. Установка зависимостей
    pip install -r requirements.txt
5. Запуск тестов
    - pytest - Запуск всех тестов
    - pytest tests/ - только API тесты
    - pytest ui/playwright/ - UI тесты Playwright
    - pytest ui/selenium/ - UI тесты Selenium



