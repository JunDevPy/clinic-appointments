ER-диаграмма базы данных:

| Column        | Type       | Описание                      |
|---------------|------------|-------------------------------|
| id            | int        | PRIMARY KEY                   |
| patient_name  | string     | Имя пациента                  |
| doctor_id     | int        | ID врача                      |
| start_time    | datetime   | Время начала приема           |
| created_at    | datetime   | Дата создания записи          |
| updated_at    | datetime   | Дата последнего обновления    |
\

Текстовое описание структуры БД:
- Таблица `appointments`
- Поля:
  - `id` (Primary Key): Уникальный идентификатор записи
  - `patient_name`: ФИО пациента
  - `doctor_id`: Идентификатор врача 
  - `start_time`: Время начала приема
  - `created_at`: Timestamp создания записи
  - `updated_at`: Timestamp обновления записи

Ограничения:
- Уникальность пары `doctor_id` + `start_time`
- `NOT NULL` для обязательных полей