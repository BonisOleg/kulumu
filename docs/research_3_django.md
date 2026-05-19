# Research · Частина 3 · Django + HTMX: структура, моделі, URL, фільтр

> Бекенд-частина архітектури kylymy. Стек: **Python 3, Django, HTMX**. Усе по чистих окремих файлах за правилом ≤500 рядків.

---

## 1. Структура Django-проєкту

```
kylymy/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── pyproject.toml
├── docs/                              # цей дослідницький документ
│
├── kylymy/                            # core project
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── catalog/                       # моделі товарів і фасетів
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── series.py              # ProductSeries (картка-серія)
│   │   │   ├── variant.py             # ProductVariant (розмір × колір)
│   │   │   ├── facet.py               # Section, Category, Style, Purpose, Form, Size, Color, Manufacturer
│   │   │   └── media.py               # ProductImage
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── home.py
│   │   │   ├── section.py             # корінь розділу
│   │   │   ├── facet.py               # фасетний listing (з фільтром HTMX)
│   │   │   ├── series.py              # картка серії
│   │   │   └── search.py
│   │   ├── filters.py                 # django-filter / власна логіка
│   │   ├── seo.py                     # генератори title/description/JSON-LD
│   │   ├── selectors.py               # query-логіка (data-access layer)
│   │   ├── services.py                # бізнес-логіка
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   │
│   ├── content/                       # блог + статичні сторінки
│   │   ├── models/
│   │   │   ├── article.py
│   │   │   ├── category.py
│   │   │   └── faq.py
│   │   ├── views/
│   │   │   ├── article_list.py
│   │   │   ├── article_detail.py
│   │   │   └── faq.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   │
│   ├── reviews/                       # відгуки
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   ├── leads/                         # форми замовлення дзвінка, "допоможіть з вибором"
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   ├── cart/                          # кошик і оформлення
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── services.py
│   │   └── urls.py
│   │
│   ├── seo/                           # sitemap, robots, schema helpers, redirects
│   │   ├── sitemaps.py
│   │   ├── views.py
│   │   ├── schema.py
│   │   └── urls.py
│   │
│   └── core/                          # спільні template-tags, context_processors, middleware
│       ├── templatetags/
│       │   ├── __init__.py
│       │   ├── kylymy_format.py       # фільтри: ціна, розмір, відсоток
│       │   ├── kylymy_seo.py          # canonical, hreflang, JSON-LD
│       │   └── kylymy_ui.py           # хлібні крихти, бейджі, карта розмірів
│       ├── context_processors.py
│       ├── middleware.py
│       └── views.py                   # 404, 500, robots
│
├── templates/                         # глобальні шаблони
│   ├── base/
│   │   ├── base.html
│   │   ├── _head.html
│   │   ├── _header.html
│   │   ├── _footer.html
│   │   ├── _meta.html
│   │   └── _scripts.html
│   ├── catalog/
│   │   ├── home.html
│   │   ├── section.html
│   │   ├── facet.html
│   │   ├── series.html
│   │   ├── partials/                  # для HTMX-перерендерів
│   │   │   ├── product_grid.html
│   │   │   ├── product_card.html
│   │   │   ├── filter_sidebar.html
│   │   │   ├── filter_chips.html
│   │   │   ├── pagination.html
│   │   │   ├── variant_swatches.html
│   │   │   └── breadcrumbs.html
│   │   └── components/
│   │       ├── badge.html
│   │       ├── price.html
│   │       └── size_grid.html
│   ├── content/
│   │   ├── article_list.html
│   │   ├── article_detail.html
│   │   └── faq.html
│   ├── reviews/
│   │   ├── _list.html
│   │   └── _form.html
│   ├── leads/
│   │   ├── callback_modal.html
│   │   └── helpme_form.html
│   ├── cart/
│   │   ├── cart.html
│   │   └── checkout.html
│   └── pages/                         # Доставка, Про нас, Контакти
│       ├── delivery.html
│       ├── about.html
│       └── contacts.html
│
├── static/                            # розкривається у Частині 4
├── media/                             # контент користувача (фото товарів)
└── locale/                            # i18n
    ├── uk/LC_MESSAGES/
    └── en/LC_MESSAGES/
```

> **Принцип розподілу файлів:** один компонент = один файл; одна view-функція = один файл; CSS-компонент = один файл. Префікси `1_`, `2_`, `3_` як вимагає правило користувача там, де файли треба підключати у певному порядку. Жоден файл — не довший за 500 рядків; якщо більший — ділимо на 2-3 з суфіксами `_1`, `_2`, `_3`.

---

## 2. Моделі (ключові)

### 2.1 `apps/catalog/models/facet.py`
```python
class Section(TimeStampedModel):                # kylymy / dorizhky / kovrolin / dlya-vannoyi
    slug_uk = models.SlugField(unique=True)
    slug_en = models.SlugField(unique=True, blank=True)
    name_uk = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80, blank=True)
    name_genitive_uk = models.CharField(max_length=80)   # "килимів", для шаблонів
    icon = models.ImageField(upload_to="sections/", blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    seo_text = models.TextField(blank=True)              # для нижнього блоку
    sort_order = models.PositiveSmallIntegerField(default=0)

class FacetType(models.TextChoices):
    CATEGORY = "category", "Тип/матеріал"
    PURPOSE  = "purpose",  "Призначення"
    STYLE    = "style",    "Стиль"
    FORM     = "form",     "Форма"
    SIZE     = "size",     "Розмір"
    COLOR    = "color",    "Колір"
    MANUFACTURER = "mfr",  "Виробник"

class Facet(TimeStampedModel):
    type = models.CharField(max_length=16, choices=FacetType.choices)
    slug_uk = models.SlugField()
    slug_en = models.SlugField(blank=True)
    name_uk = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80, blank=True)
    is_indexable = models.BooleanField(default=True)     # whitelist для SEO
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    sort_order = models.PositiveSmallIntegerField(default=0)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    seo_text = models.TextField(blank=True)              # унікальний текст під каталогом
    class Meta:
        unique_together = ("type", "slug_uk")
        indexes = [models.Index(fields=["type", "is_indexable"])]
```

### 2.2 `apps/catalog/models/series.py`
```python
class ProductSeries(TimeStampedModel):
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    slug_uk = models.SlugField()
    slug_en = models.SlugField(blank=True)
    name = models.CharField(max_length=120)               # "Shaggy Roco"
    short_descr = models.TextField(blank=True)
    full_descr = models.TextField(blank=True)
    care_instructions = models.TextField(blank=True)

    facets = models.ManyToManyField(Facet, related_name="series")    # тип / стиль / призначення / форма / виробник
    primary_color = models.ForeignKey(Facet, on_delete=models.SET_NULL, null=True, related_name="+")
    pile_height_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    base_material = models.CharField(max_length=80, blank=True)      # джут / повсть / гума
    composition = models.CharField(max_length=120, blank=True)       # поліпропілен 100%
    country = models.CharField(max_length=40, blank=True)
    weight_per_m2 = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    discount_percent = models.PositiveSmallIntegerField(default=0)

    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    class Meta:
        unique_together = ("section", "slug_uk")
        indexes = [models.Index(fields=["section", "is_active"])]
```

### 2.3 `apps/catalog/models/variant.py`
```python
class ProductVariant(TimeStampedModel):
    series = models.ForeignKey(ProductSeries, related_name="variants", on_delete=models.CASCADE)
    sku = models.CharField(max_length=64, unique=True)
    color = models.ForeignKey(Facet, on_delete=models.PROTECT, related_name="+")
    size = models.ForeignKey(Facet, on_delete=models.PROTECT, related_name="+")  # 0.8x1.5, 1.6x2.3 і т.д.
    width_cm = models.PositiveSmallIntegerField()
    length_cm = models.PositiveSmallIntegerField(null=True, blank=True)          # null для "на відріз"
    is_per_meter = models.BooleanField(default=False)                            # пог.м

    price_uah = models.PositiveIntegerField()
    old_price_uah = models.PositiveIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    ready_to_ship = models.BooleanField(default=True)

    image = models.ImageField(upload_to="variants/", blank=True)
```

### 2.4 `apps/catalog/models/media.py`
```python
class ProductImage(TimeStampedModel):
    series = models.ForeignKey(ProductSeries, related_name="images", on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    alt = models.CharField(max_length=160)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
```

### 2.5 `apps/content/models/article.py`
```python
class ArticleCategory(TimeStampedModel):
    slug_uk = models.SlugField(unique=True)
    name_uk = models.CharField(max_length=80)

class Article(TimeStampedModel):
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True)
    slug_uk = models.SlugField(unique=True)
    title_uk = models.CharField(max_length=200)
    cover = models.ImageField(upload_to="articles/")
    excerpt = models.CharField(max_length=300)
    body = models.TextField()                          # markdown або rich-text
    related_facets = models.ManyToManyField(Facet, blank=True)
    related_series = models.ManyToManyField(ProductSeries, blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
```

### 2.6 `apps/reviews/models.py`
```python
class Review(TimeStampedModel):
    series = models.ForeignKey(ProductSeries, related_name="reviews", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=80)
    rating = models.PositiveSmallIntegerField(default=5)         # 1-5
    body = models.TextField()
    photo = models.ImageField(upload_to="reviews/", blank=True)
    is_approved = models.BooleanField(default=False)
```

### 2.7 `apps/leads/models.py`
```python
class CallbackRequest(TimeStampedModel):
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=32)
    page_url = models.URLField(blank=True)
    series = models.ForeignKey(ProductSeries, null=True, blank=True, on_delete=models.SET_NULL)
    is_processed = models.BooleanField(default=False)
```

---

## 3. URL routing (`kylymy/urls.py`)

```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap_index.xml", sitemap_index_view),
    path("sitemap_<str:section>.xml", sitemap_section_view),
    path("robots.txt", robots_view),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("apps.catalog.urls")),         # головна, розділи, фасети, серії
    path("blog/", include("apps.content.urls")),
    path("faq/", faq_view, name="faq"),
    path("dostavka-i-oplata/", delivery_view),
    path("pro-nas/", about_view),
    path("kontakty/", contacts_view),
    path("akciyi/", actions_view),
    path("kylymy/", include("apps.cart.urls")),
    path("leads/", include("apps.leads.urls")),
    prefix_default_language=False,                  # /uk/ — без префіксу для default
)
```

`apps/catalog/urls.py` (ключові маршрути):
```python
urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("<slug:section_slug>/", SectionView.as_view(), name="section"),
    path("<slug:section_slug>/<slug:facet_slug>/", FacetView.as_view(), name="facet1"),
    path("<slug:section_slug>/<slug:f1>/<slug:f2>/", FacetView.as_view(), name="facet2"),
    path("<slug:section_slug>/seriya/<slug:series_slug>/", SeriesView.as_view(), name="series"),

    path("search/", SearchView.as_view(), name="search"),

    # HTMX endpoints (повертають partial HTML)
    path("htmx/filter/", filter_partial_view, name="htmx_filter"),
    path("htmx/series/<int:series_id>/variant/", variant_partial_view, name="htmx_variant"),
    path("htmx/calc/<int:series_id>/", per_meter_calc_view, name="htmx_calc"),
]
```

---

## 4. HTMX — фільтр без перезавантаження сторінки

### 4.1 Поведінка
1. Користувач клікає чекбокс/радіо у `#filter-sidebar` або змінює range "ціна".
2. Подія `change` тригерить `hx-get="/htmx/filter/"` з усіма поточними параметрами фільтра + `hx-push-url="true"` (щоб URL у браузері і Google ботові оновлювалися).
3. Сервер віддає `partials/product_grid.html` + `partials/filter_chips.html` + `partials/pagination.html` (multi-swap через `hx-swap-oob` або `HX-Trigger` подію).
4. Заголовки відповіді включають оновлений canonical (для подальших серверних рендерів).

### 4.2 Приклад розмітки
```html
<!-- catalog/facet.html -->
<aside id="filter-sidebar"
       hx-get="{% url 'htmx_filter' %}"
       hx-trigger="change from:input from:select from:#price-range delay:300ms"
       hx-target="#products-area"
       hx-swap="innerHTML"
       hx-push-url="true">
  {% include "catalog/partials/filter_sidebar.html" %}
</aside>

<section id="products-area">
  {% include "catalog/partials/breadcrumbs.html" %}
  {% include "catalog/partials/filter_chips.html" %}
  {% include "catalog/partials/product_grid.html" %}
  {% include "catalog/partials/pagination.html" %}
</section>
```

### 4.3 SEO-нюанси
- **Initial render — повноцінний HTML** (не порожній shell). Google бот бачить товари без виконання JS.
- HTMX лише вмикає інтерактивне оновлення.
- `hx-push-url` синхронізує URL у браузері з фільтром, що робить можливим поділитись посиланням, додати в закладки, віднайти у Search Console.
- Canonical залишається на основній фасетній URL (без query) — індексується одна, а UX-варіанти — `noindex,follow`.
- Для пагінації — `hx-target="#products-area" hx-swap="outerHTML"` + `hx-push-url`.

### 4.4 Оптимізація запитів
- На бекенді — один queryset з `select_related("section")` + `prefetch_related("variants__color", "variants__size", "facets", "images")`.
- Кешуємо результат фасетного фільтра у Redis з ключем = sorted(query_params) на 5-15 хв.
- Інвалідація кешу через сигнал `post_save` на `ProductSeries` / `ProductVariant`.

---

## 5. Адмінка (Django Admin кастомізація)

- **list_display + list_filter** на `ProductSeries` (section, is_active, is_top, is_new, discount_percent)
- **TabularInline** для `ProductVariant` під серією (з ціновим розрахунком на льоту)
- **TabularInline** для `ProductImage` під серією (drag-and-drop сортування — django-admin-sortable2)
- **autocomplete_fields** для `Facet` за типом фасету (інакше випадайка з 200+ значень буде непридатна)
- **Pre-save сигнал** генерує `slug_uk` через `python-slugify` з `unidecode`, перевіряє унікальність у межах section
- **Bulk-дії**: "Опублікувати", "Зняти знижку", "Зробити топом", "Експортувати в XML feed" (для Prom/Rozetka/Google Merchant)
- Окремий розділ адмінки **"SEO"**: ручні `seo_title`/`seo_description` для будь-якої сторінки + перегляд згенерованих за шаблоном
- Розділ **"Ліди"** з фільтром по непрочитаних, експорт у CSV, інтеграція з Telegram-сповіщенням

---

## 6. Безпека

- **Django security middleware** в усіх dev/prod конфігах
- **CSP-заголовки** (django-csp): заборона inline JS окрім nonced; allow-list домени для GTM/GA/LiqPay
- **HSTS**, **X-Frame-Options=SAMEORIGIN**, **X-Content-Type-Options=nosniff**, **Referrer-Policy=strict-origin-when-cross-origin**
- **Rate limiting** на формах (django-ratelimit): 5 запитів/хв на лідогенераційні форми по IP
- **CSRF** на всіх state-changing операціях (включно з HTMX через `hx-headers='{"X-CSRFToken": "..."}'`)
- **DEBUG=False у prod**, окремий SECRET_KEY через .env
- **Захист від SSRF** при роботі з зовнішніми API (Нова Пошта)
- **Sentry** для моніторингу помилок

---

## 7. Продуктивність

| Шар             | Рішення                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------- |
| DB              | PostgreSQL 16, GIN-індекси на M2M (facets), `select_related`/`prefetch_related` обов'язкові              |
| Кеш             | Redis: фасети — 1h, картка серії — 1h, головна — 30 хв; інвалідація через сигнали                        |
| Static          | WhiteNoise + nginx, `Cache-Control: max-age=31536000, immutable`                                          |
| Зображення      | Pillow + сигнал post_save → WebP + 3 розміри (400/800/1200 px ширини). Можна django-imagekit.            |
| HTML            | Стиснення gzip/brotli на nginx                                                                            |
| Шаблони         | `cached_template_loader` у prod                                                                           |
| LCP-зображення  | preload у `<head>`, `fetchpriority="high"` на `<img>`                                                    |
| 3rd-party JS    | GTM з `defer`, асинхронні чат-віджети, ніколи `<script>` синхронно у head                                |
| HTML розмір     | < 100 КБ на категорії (без зображень), < 60 КБ на картці                                                  |

**Lighthouse цілі:** Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95 на 5 типах сторінок.

---

## 8. Тести

- **pytest + pytest-django** як основний стек
- **factory-boy** для фікстур (SeriesFactory, VariantFactory, FacetFactory)
- Покриття:
  - selectors.py — unit-тести query-логіки
  - SEO-генератори — unit-тести title/description/JSON-LD
  - URL — smoke-тести 200 на ключових сторінках
  - HTMX — тести partial-view (повертають правильний HTML-фрагмент)
  - Форми лідогенерації — валідація + ratelimit
- CI: GitHub Actions → ruff + black + djlint + pytest на кожен PR

---

> **Далі — Частина 4** (`research_4_frontend.md`): mobile-first CSS (iOS Safari), JavaScript, інтеграції, MVP-чек-лист, фішки, requirements.txt.
