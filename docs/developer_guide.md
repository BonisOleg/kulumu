# Посібник розробника Kylymy

## Як додати новий тип фасету

1. Відкрий `apps/catalog/models/facet.py` → `FacetType`
2. Додай нове значення:
   ```python
   MY_TYPE = "my_type", _("Мій тип")
   ```
3. Додай SQL через міграцію:
   ```bash
   python manage.py makemigrations catalog
   python manage.py migrate
   ```
4. У адмінці (Facet) вже буде новий тип у випадайці.

## Як додати нову статичну сторінку

1. Відкрий `apps/content/models/page.py` → `SLUG_CHOICES`
2. Додай slug: `("my-page", "Моя сторінка")`
3. Виконай міграцію
4. Через адмінку **Статичні сторінки** → **+** → обери slug → заповни контент

## Як змінити SEO-шаблон title для категорій

Відкрий `apps/catalog/models/series.py`:
```python
def get_seo_title(self):
    if self.seo_title:
        return self.seo_title
    return f"{self.name} — купити в Україні | Kylymy"  # ← змінити тут
```

## Як перекласти контент на другу мову

1. `MODELTRANSLATION_LANGUAGES` в `settings/base.py` вже містить `("uk", "en")`
2. В адмінці поля відображаються з вкладками UA / EN
3. Для активації EN URL-prefix: в `settings/base.py` у `LANGUAGES` та у `kylymy/urls.py` через `i18n_patterns`

## Як додати новий CSS-компонент

1. Створи файл `static/css/components/my_component.css` (не більше 500 рядків)
2. Підключи у `templates/base/_head.html` у відповідному місці
3. Ніколи не використовуй `!important`

## Деплой на Render (PaaS)

Див. **`docs/deploy_render.md`** та **`render.yaml`**. Медіа в проді — через **Cloudinary** (`CLOUDINARY_URL`).

## Як налаштувати prod-деплой

1. Скопіюй `deploy/gunicorn-kylymy.service` у `/etc/systemd/system/`
2. Скопіюй `nginx/prod.conf` у `/etc/nginx/sites-available/kylymy`
3. `sudo ln -s /etc/nginx/sites-available/kylymy /etc/nginx/sites-enabled/`
4. `sudo certbot --nginx -d kylymy.ua -d www.kylymy.ua`
5. `sudo systemctl enable gunicorn-kylymy && sudo systemctl start gunicorn-kylymy`
6. Встанови cron для бекапу: `0 3 * * * /var/www/kylymy/deploy/backup.sh`

## Конфігурація GitHub Secrets для auto-deploy

У GitHub репозиторії → Settings → Secrets and variables → Actions:
- `PROD_HOST` — IP або домен сервера
- `PROD_USER` — ssh username (зазвичай `www-data` або `deploy`)
- `PROD_SSH_KEY` — приватний SSH-ключ без passphrase
