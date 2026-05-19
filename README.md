# Kylymy — інтернет-магазин килимів

Django + HTMX e-commerce з преміальною адмінкою `django-unfold`.

## Стек

- Python 3.12+, Django 5.x
- PostgreSQL 16, Redis 7
- HTMX 2.x (без бандлера)
- django-unfold + django-modeltranslation + django-tinymce
- Нова Пошта API, LiqPay/WayForPay
- nginx + gunicorn + WhiteNoise

## Запуск (розробка)

```bash
# 1. Клонувати репозиторій
git clone https://github.com/your-org/kylymy.git
cd kylymy

# 2. Налаштувати .env
cp .env.example .env
# Відредагувати .env з вашими SECRET_KEY тощо

# 3. Встановити залежності
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt

# 4. Застосувати міграції
python manage.py migrate

# 5. Наповнити демо-даними
python manage.py seed_demo

# 6. Створити суперюзера
python manage.py createsuperuser

# 7. Зібрати статику
python manage.py collectstatic --noinput

# 8. Запустити сервер
python manage.py runserver
```

Відкрити: http://localhost:8000

Адмінка: http://localhost:8000/admin/

## Запуск через Docker

```bash
cp .env.example .env
# Відредагуйте .env (DATABASE_URL, REDIS_URL замість localhost → db, redis)
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py createsuperuser
```

## Структура проєкту

```
kylymy/
├── apps/
│   ├── catalog/          # Товари: Section, Facet, ProductSeries, ProductVariant, ProductImage
│   ├── content/          # Блог, FAQ, статичні сторінки
│   ├── reviews/          # Відгуки з модерацією
│   ├── leads/            # Форми зворотного зв'язку
│   ├── cart/             # Кошик і замовлення
│   ├── seo/              # Sitemap, robots.txt
│   ├── core/             # SiteSettings, templatetags, context_processors
│   ├── adminconf/        # Конфіг django-unfold
│   └── integrations/     # НП API, LiqPay, Telegram, Email
├── docs/                 # Документи дослідження ринку
├── static/               # CSS, JS, фото
├── templates/            # HTML-шаблони
├── locale/               # i18n (UK, EN)
├── nginx/                # nginx конфіги
└── requirements/         # base, dev, prod
```

## Ключові команди

```bash
# Демо-дані
python manage.py seed_demo

# Міграції
python manage.py makemigrations
python manage.py migrate

# Синхронізація перекладів modeltranslation
python manage.py update_translation_fields

# Збір статики
python manage.py collectstatic --noinput

# Тести
pytest
pytest --cov=apps --cov-report=html

# Лінтер
ruff check .
djlint templates/ --profile django
```

## Production: Render + Cloudinary

- Кореневий `requirements.txt` і `runtime.txt` — для **Render Native Python**.
- `render.yaml` — Blueprint (Web + Postgres + Key Value для Redis).
- `scripts/render_build.sh` / `scripts/render_release.sh` — збірка та міграції.
- Медіа в проді: змінна **`CLOUDINARY_URL`** → `django-cloudinary-storage` (див. `kylymy/settings/prod.py`).

Повний чеклист і змінні середовища: **`docs/deploy_render.md`**.

## Правила розробки

- Кожен файл — не більше 500 рядків (розбивати на _1, _2, _3)
- Без `!important` у CSS
- Mobile-first, iOS Safari як еталон
- `unfold` — ЗАВЖДИ перед `django.contrib.admin` в `INSTALLED_APPS`
- Тільки `django-tinymce` для WYSIWYG (ніколи CKEditor)
- Без кастомних CSS/JS в адмінці (тільки вбудовані засоби unfold)
- Тільки стандартна авторизація Django (без `django-guardian`)
