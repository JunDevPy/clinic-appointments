# Тестовое задание - Clinic Appointments 

Микросервис на FastAPI для записи пациентов к врачам (PostgreSQL).

## Быстрый старт (~1 минута)

```bash
git clone <repository-url>
cd clinic-appointments
cp .env.example .env
docker-compose up -d --build
curl http://localhost:8000/health
Если всё в порядке, вернётся HTTP 200 и { "status": "ok" }.
```

## Команды Makefile

- `make lint` — проверка стиля (black, isort, flake8)
- `make test` — запуск тестов (pytest)
- `make up` — поднять сервисы (docker-compose)
- `make down` — остановить сервисы
- `make migrate` — создать схемы в БД
- `make clean` — удалить контейнеры и очищает docker


## API
```GET /health``` - Проверка здоровья сервиса.

```POST /appointments``` - Создать новую запись.

`Request body (application/json)` : 
`{
  "patient_name": "Иван Иванов",
  "doctor_id": 1,
  "start_time": "2025-07-10T10:00:00"
}`

**Уникальность пары doctor_id + start_time проверяется на уровне БД.**

`GET /appointments/{id}` - Получить запись по ID.

**_Пример запроса:_**

```code
curl -X POST http://localhost:8000/appointments \
  -H "Content-Type: application/json" \
  -d '{"patient_name":"Иван Иванов","doctor_id":1,"start_time":"2025-07-10T10:00:00"}'
  ```

`curl http://localhost:8000/appointments/1`

## Структура проекта
```
.
├── .env.example                              # Пример файла с переменными для деплоя
├── Dockerfile
├── docker-compose.yml
├── Makefile                                  # Быстрые команды Make
├── LICENSE                                   # Описание лицензии
├── README.md                                 # Этот файл
├── requirements.txt                          # Зависимости
├── bot/
│   ├── bot.py                                # stub-пакет для Telegramm бота
│   ├── this_bot_dialog_from_example.md       # Пример диалога с Telegramm ботом
├── docs/
│   ├── activity-diagramm.md                  # Activity-диаграмма описание
│   ├── activity-diagramm.png                 # Activity-диаграмма рисунок PNG
│   ├── answers.txt                           # Ответы на Короткий опросник из ТЗ
│   ├── architecture-schema.md                # Архитектурная схема
│   ├── architecture-schema.png               # Архитектурная схема рисунок PNG
│   ├── business-process.md                   # Описание бизнес-процесса 
│   ├── business-process.png                  # Описание бизнес-процесса рисунок PNG
│   ├── er-diagramm.md                        # ER-диаграмма базы данных
├── api/
│   ├── main.py                               # точка входа FastAPI
│   ├── auth.py                               # Авторизация JWT
│   ├── config.py                             # Конфиг для чтения env
│   ├── models.py                             # ORM-модель Appointment
│   ├── schemas.py                            # Pydantic-схемы
│   ├── crud.py                               # CRUD-операции
│   ├── database.py                           # подключение к БД
│   └── exceptions.py                         # Обработка исключений
├── tests/
│   ├── test_models.py                        # Тесты для моделей
│   └── test_api.py                           # Тесты для Эндпоинтов
└── .github/
    └── workflows/ci.yml                      # CI\CD GitHub Actions
```

## CI/CD
_**GitHub Actions запускает две задачи:**_

`lint (black, isort, flake8)` \
`test (pytest)` \

**В обоих шагах требуется ноль ошибок, после этого пушим контейнер (при необходимости).**



