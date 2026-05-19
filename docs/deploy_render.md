# Деплой Kylymy на Render + Cloudinary

Короткий чеклист для production: **PostgreSQL**, **Redis**, **WhiteNoise** (статика), **Cloudinary** (медіа), **Gunicorn** за `$PORT`.

## 1. Обліковий запис і репозиторій

1. Зареєструйся на [Render](https://render.com), підключи GitHub/GitLab.
2. Переконайся, що в репозиторії є `render.yaml`, `requirements.txt`, `runtime.txt`, `scripts/render_build.sh`.

## 2. Cloudinary (медіа: фото товарів, статті, відгуки)

1. Створи безкоштовний акаунт на [Cloudinary](https://cloudinary.com).
2. У Dashboard скопіюй **Environment variable** `CLOUDINARY_URL` (формат `cloudinary://api_key:api_secret@cloud_name`).
3. У Render → Web Service → **Environment** додай змінну `CLOUDINARY_URL` з цим значенням.

Якщо `CLOUDINARY_URL` **не** задано, прод використовує локальний диск `MEDIA_ROOT` (на Render без постійного тома файли зникнуть після рестарту — для медіа Cloudinary **обовʼязковий**).

## 3. Змінні середовища на Render (мінімум)

| Змінна | Приклад / примітка |
|--------|-------------------|
| `DJANGO_SETTINGS_MODULE` | `kylymy.settings.prod` |
| `SECRET_KEY` | Довгий випадковий рядок (Render може згенерувати в Blueprint) |
| `ALLOWED_HOSTS` | `kylymy-web.onrender.com` або власний домен через кому |
| `SITE_URL` | `https://kylymy-web.onrender.com` (публічний HTTPS URL) |
| `CSRF_TRUSTED_ORIGINS` | `https://kylymy-web.onrender.com` (той самий origin, без слешу в кінці) |
| `DATABASE_URL` | Зазвичай зʼявляється автоматично при лінкуванні Postgres |
| `REDIS_URL` | З Redis add-on / Blueprint |
| `CLOUDINARY_URL` | З Cloudinary Dashboard |
| `SENTRY_DSN` | Опційно, для моніторингу помилок |

Інтеграції (Nova Poshta, LiqPay, Telegram, пошта) — за потреби з `.env.example`.

## 4. Міграції та суперкористувач

Після першого успішного деплою:

1. У Render відкрий **Shell** для web-сервісу або додай одноразову **Post-Deploy** команду.
2. Виконай:

```bash
export DJANGO_SETTINGS_MODULE=kylymy.settings.prod
python manage.py migrate --noinput
python manage.py createsuperuser
```

Демо-дані (опційно): `python manage.py seed_demo`

## 5. Власний домен

У Render → **Custom Domains** додай домен, онови `ALLOWED_HOSTS`, `SITE_URL`, `CSRF_TRUSTED_ORIGINS` на `https://твій-домен.ua`.

## 6. Діагностика

- Логи: Render Dashboard → Logs.
- Статика не зʼявляється: перевір `collectstatic` у логах збірки; `DEBUG` має бути `False`.
- 403 CSRF: перевір `CSRF_TRUSTED_ORIGINS` і збіг з URL у браузері.
- Медіа 404 без Cloudinary: задай `CLOUDINARY_URL`.

## 7. Локальна перевірка «як на проді»

```bash
export DJANGO_SETTINGS_MODULE=kylymy.settings.prod
export DATABASE_URL=postgres://...
export REDIS_URL=redis://...
export CLOUDINARY_URL=cloudinary://...
export SECRET_KEY=...
export ALLOWED_HOSTS=localhost,127.0.0.1
export SITE_URL=http://127.0.0.1:8000
pip install -r requirements/prod.txt
python manage.py migrate
python manage.py runserver
```

---

Деталі реалізації: `kylymy/settings/prod.py` (Cloudinary через `STORAGES`, проксі-заголовки), `kylymy/wsgi.py` (режим prod за наявності `RENDER`).
