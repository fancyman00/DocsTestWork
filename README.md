# DocsTestWork

Тестовое задание: REST API для учёта **документов** и **связей между ними**.

Стек: **Flask** + **PostgreSQL** (psycopg2). Слои: API → Controller → Database.

## Возможности

- CRUD документов (`content`, `header`, `type`)
- Типы документов: входящий / исходящий / внутренний
- Связи между документами (`doc_links`)
- Логирование запросов (singleton-логгер)
- Декораторы валидации payload и обработки ошибок

## Структура

```
DocsTestWork/
├── __main__.py          # Flask app, подключение БД, запуск
├── docs/
│   ├── api.py           # HTTP-роуты /document
│   ├── controller.py    # SQL + маппинг ответа
│   ├── model.py         # dataclass DocumentModel
│   └── enums.py         # Types, Links
└── tools/
    ├── database.py      # обёртка над psycopg2
    ├── request.py       # required_payload, error
    ├── logger.py        # логгер запросов
    └── singelton.py     # metaclass Singleton
```

## Модель данных

### Документ (`docs`)

| Поле | Описание |
|------|----------|
| `id` | PK (`nextval('unique_id')`) |
| `content` | текст |
| `header` | заголовок |
| `type` | `1` IN / `2` OUT / `3` INNER |

### Связь (`doc_links`)

| Поле | Описание |
|------|----------|
| `id` | id исходного документа |
| `type` | тип связи (IN_OUT / OUT_IN / INNER_INNER) |
| `link_id` | id связанного документа |

Типы связей (человекочитаемые имена в `enums.py`):

- `1` — Входящий-Исходящий
- `2` — Исходящий-Входящий
- `3` — Внутренний-Внутренний

## API

Базовый префикс: `/document`  
Сервер по умолчанию: `http://localhost:8081`

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/document/<id>` | Документ по id (+ links) |
| `GET` | `/document?count=N` | Список (опционально лимит `count`) |
| `POST` | `/document` | Создать документ |
| `PUT` | `/document/<id>` | Обновить документ |
| `DELETE` | `/document/<id>` | Удалить документ |
| `POST` | `/document/link/<id>` | Создать связь |
| `DELETE` | `/document/link/<id>` | Удалить связь |

### Примеры

**Создать документ**

```http
POST /document
Content-Type: application/json

{
  "content": "Текст документа",
  "header": "Заголовок",
  "type": 1
}
```

**Обновить документ**

```http
PUT /document/42
Content-Type: application/json

{
  "content": "Новый текст",
  "header": "Новый заголовок",
  "type": 2
}
```

**Создать связь**

```http
POST /document/link/42
Content-Type: application/json

{
  "type": 1,
  "link_id": 10
}
```

**Список с лимитом**

```http
GET /document?count=10
```

Ответ документа (пример):

```json
{
  "id": 1,
  "content": "...",
  "header": "...",
  "type": "Входящий",
  "links": [
    { "document_id": 10, "link_type": 1 }
  ]
}
```

## Быстрый старт

### 1. PostgreSQL

Нужны таблицы `docs`, `doc_links` и sequence `unique_id` (создаются вне репозитория / вручную).

Пример схемы:

```sql
CREATE SEQUENCE unique_id;

CREATE TABLE docs (
    id INTEGER PRIMARY KEY,
    content TEXT,
    header TEXT,
    type INTEGER
);

CREATE TABLE doc_links (
    id INTEGER,
    type INTEGER,
    link_id INTEGER
);
```

### 2. Окружение

```bash
git clone https://github.com/fancyman00/DocsTestWork.git
cd DocsTestWork

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# укажите DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
```

### 3. Запуск

```bash
python __main__.py
# → http://localhost:8081
```

Логи пишутся в `logger.log`.

## Стек

- Python 3
- Flask
- PostgreSQL + psycopg2
- python-dotenv (конфиг БД)

## Статус

Учебное / тестовое задание. Не production-ready:

- нет миграций Alembic и готового SQL-дампа в репо
- ошибки API отдаются как HTTP 500 с текстом исключения
- `type` / `link_type` в связях возвращаются числом, тип документа — строкой

## Лицензия

MIT
