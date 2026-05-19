# Research · Частина 4 · Frontend, інтеграції, MVP

> Фронт-частина: mobile-first CSS (iOS Safari), JS-модулі, інтеграції, MVP чек-лист, фішки, залежності.

---

## 1. Структура `static/`

```
static/
├── css/                                  # БЕЗ !important
│   ├── 1_reset.css
│   ├── 2_tokens.css                      # CSS-змінні: кольори, типографіка, spacing
│   ├── 3_base.css
│   ├── 4_layout.css
│   ├── 5_typography.css
│   ├── components/                       # один компонент = один файл
│   │   ├── header.css
│   │   ├── footer.css
│   │   ├── product_card.css
│   │   ├── product_grid.css
│   │   ├── filter_sidebar.css
│   │   ├── filter_chips.css
│   │   ├── breadcrumbs.css
│   │   ├── badge.css
│   │   ├── price.css
│   │   ├── button.css
│   │   ├── modal.css
│   │   ├── drawer.css
│   │   ├── form.css
│   │   ├── pagination.css
│   │   ├── tabs.css
│   │   ├── gallery.css
│   │   └── article.css
│   └── pages/
│       ├── home.css
│       ├── section.css
│       ├── facet.css
│       ├── series.css
│       ├── article.css
│       └── checkout.css
│
├── js/                                   # модульні файли, кожен ≤500 рядків
│   ├── main.js                           # entry, ініціалізація
│   ├── modules/
│   │   ├── htmx_setup.js
│   │   ├── drawer.js
│   │   ├── modal.js
│   │   ├── filter_chips.js
│   │   ├── variant_swatch.js
│   │   ├── price_calculator.js           # для доріжок на відріз
│   │   ├── lazy_images.js                # IntersectionObserver-fallback
│   │   ├── safari_fix.js                 # iOS-quirks (-webkit-overflow-scrolling, 100dvh)
│   │   └── lead_form.js
│   └── vendor/
│       └── htmx.min.js
│
├── icons/
│   └── sprite.svg
├── images/
└── fonts/
```

---

## 2. Mobile-first CSS

### 2.1 Загальні правила (зі сторони користувача)
- **Жодного `!important`** (за правилом користувача). Каскад керується специфічністю + порядком підключення (`1_reset → 2_tokens → 3_base → 4_layout → 5_typography → components/ → pages/`).
- CSS-змінні (`2_tokens.css`) для кольорів, шрифтів, тіней, заокруглень, breakpoints.
- Breakpoints (mobile → desktop):
  - `0–599px` — phone (default стилі без media-query)
  - `600–959px` — tablet
  - `960–1279px` — small desktop
  - `1280px+` — desktop
- Patterns:
  - **mobile-first**: базові стилі для phone; розширюємо `@media (min-width: 600px)`, `@media (min-width: 960px)`, `@media (min-width: 1280px)`.
  - **CSS Grid** для каталогу (`auto-fill, minmax(...)` дозволяє адаптуватись без media-query).
  - **CSS Container Queries** для карток товару (працює на нових iOS).
  - Всі інтерактивні елементи мають `min-height: 44px` (Apple HIG).

### 2.2 `2_tokens.css`
```css
:root {
  /* viewport з урахуванням адресного рядка iOS */
  --vh: 100dvh;
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
  --safe-right: env(safe-area-inset-right, 0px);

  /* кольори */
  --c-bg: #fafaf7;
  --c-surface: #ffffff;
  --c-text: #1a1a1a;
  --c-muted: #6b6b6b;
  --c-border: #e6e2dc;
  --c-accent: #b48a5e;            /* теплий, килимовий */
  --c-accent-hover: #9d7244;
  --c-danger: #c44343;
  --c-success: #4f8a4a;
  --c-badge-new: #4f8a4a;
  --c-badge-top: #b48a5e;
  --c-badge-discount: #c44343;

  /* типографіка */
  --ff-base: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", system-ui, sans-serif;
  --ff-display: "Manrope", var(--ff-base);
  --fs-xs: 12px;
  --fs-sm: 14px;
  --fs-md: 16px;
  --fs-lg: 18px;
  --fs-xl: 22px;
  --fs-h2: clamp(20px, 3vw, 28px);
  --fs-h1: clamp(24px, 4vw, 36px);
  --lh-tight: 1.2;
  --lh-base: 1.5;

  /* spacing */
  --sp-1: 4px;
  --sp-2: 8px;
  --sp-3: 12px;
  --sp-4: 16px;
  --sp-5: 24px;
  --sp-6: 32px;
  --sp-8: 48px;
  --sp-10: 64px;

  /* розміри */
  --r-xs: 4px;
  --r-sm: 8px;
  --r-md: 12px;
  --r-lg: 20px;
  --r-pill: 999px;

  --shadow-sm: 0 1px 2px rgba(0,0,0,.06);
  --shadow-md: 0 6px 16px rgba(0,0,0,.08);
  --shadow-lg: 0 16px 40px rgba(0,0,0,.12);
}
```

### 2.3 iOS Safari фікси (обов'язково)
```css
/* 3_base.css */
html, body {
  min-height: 100dvh;            /* фолбек для не-iOS */
  min-height: var(--vh);
  -webkit-text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  background: var(--c-bg);
  color: var(--c-text);
  font-family: var(--ff-base);
  font-size: var(--fs-md);
  line-height: var(--lh-base);
}

* { -webkit-tap-highlight-color: transparent; }

/* інакше iOS зумить при focus на input <16px */
input, textarea, select, button {
  font-size: 16px;
  -webkit-appearance: none;
  appearance: none;
  border-radius: 0;
}

/* sticky header без jitter на iOS */
.header {
  position: sticky;
  top: 0;
  padding-top: var(--safe-top);
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  z-index: 50;
}

/* sticky bottom CTA з safe-area для нотча/home-indicator */
.cta-bar {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  padding: var(--sp-3);
  padding-bottom: max(var(--sp-3), var(--safe-bottom));
  padding-left: max(var(--sp-3), var(--safe-left));
  padding-right: max(var(--sp-3), var(--safe-right));
  background: var(--c-surface);
  box-shadow: var(--shadow-lg);
  z-index: 40;
}

/* drawer-меню зі скролом, що не лагає на iOS */
.drawer__inner {
  height: 100dvh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}

/* модалка з блокуванням body-scroll */
body.modal-open { position: fixed; width: 100%; }

/* form-elements, що нормально виглядають на iOS */
.input,
.select,
.textarea {
  width: 100%;
  padding: var(--sp-3) var(--sp-4);
  border: 1px solid var(--c-border);
  border-radius: var(--r-sm);
  background: var(--c-surface);
  font-family: inherit;
  font-size: 16px;
  line-height: var(--lh-base);
  transition: border-color .15s ease, box-shadow .15s ease;
}
.input:focus,
.select:focus,
.textarea:focus {
  outline: none;
  border-color: var(--c-accent);
  box-shadow: 0 0 0 3px rgba(180, 138, 94, 0.18);
}
```

### 2.4 Каталог-сітка (responsive без media)
```css
/* components/product_grid.css */
.product-grid {
  display: grid;
  gap: var(--sp-4);
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));   /* phone: 2 колонки */
}
@media (min-width: 600px) {
  .product-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
}
@media (min-width: 960px) {
  .product-grid { grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: var(--sp-5); }
}
@media (min-width: 1280px) {
  .product-grid { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--sp-6); }
}
```

### 2.5 Зображення (Core Web Vitals)
- Усі фото — через `<picture>` з WebP + fallback JPG.
- `loading="lazy"` крім першого fold (обов'язково `eager` для LCP).
- `width` і `height` атрибути обов'язкові (CLS=0).
- CSS `aspect-ratio: 4/3;` для картки товару.
- Pillow-генератор thumbnail у трьох розмірах: `400`, `800`, `1200` px ширини.

### 2.6 Шрифти
- Системний стек + один кастомний для logo/heading через `font-display: swap`.
- preload основного шрифту: `<link rel="preload" as="font" type="font/woff2" crossorigin>`.
- Subset кирилиці (Latin-Ext + Cyrillic), щоб не тягнути 200 КБ латиниці.

### 2.7 Доступність (a11y)
- Контраст ≥ 4.5:1 для тексту (WCAG AA)
- Усі іконки-кнопки мають `aria-label`
- Focus-стилі видимі (не `outline: none` без альтернативи)
- `prefers-reduced-motion` поважається для анімацій
- Семантичні теги: `<nav>`, `<main>`, `<aside>`, `<article>`, `<section>`

---

## 3. JavaScript (модульно, без бандлера для MVP)

### 3.1 `static/js/main.js`
```js
import { initDrawer } from "./modules/drawer.js";
import { initModal } from "./modules/modal.js";
import { initFilterChips } from "./modules/filter_chips.js";
import { initVariantSwatch } from "./modules/variant_swatch.js";
import { initPriceCalc } from "./modules/price_calculator.js";
import { initLazy } from "./modules/lazy_images.js";
import { initSafariFix } from "./modules/safari_fix.js";

document.addEventListener("DOMContentLoaded", () => {
  initSafariFix();        // обов'язково першим
  initDrawer();
  initModal();
  initFilterChips();
  initVariantSwatch();
  initPriceCalc();
  initLazy();
});
```

### 3.2 `safari_fix.js`
```js
export function initSafariFix() {
  // оновлюємо --vh при resize/orientation (для фолбеку без 100dvh)
  const setVh = () => document.documentElement.style.setProperty(
    "--vh", `${window.innerHeight}px`
  );
  setVh();
  window.addEventListener("resize", setVh, { passive: true });
  window.addEventListener("orientationchange", setVh, { passive: true });

  document.body.classList.add("ios-ready");
}
```

### 3.3 `price_calculator.js` (для доріжок на відріз)
- Слухає зміну ширини (radio) і довжини (input number з 0.1 m кроком)
- Обчислює ціну у реальному часі: `price_per_lin_m × length_m`
- Оновлює відображення без перезавантаження
- Передає значення у форму "Купити" перед submit
- Плюс HTMX-варіант для фінальної звірки на сервері

### 3.4 `variant_swatch.js`
- Кліки на color/size swatch міняють поточний варіант
- Оновлюють фото, ціну, наявність, артикул через partial-render (HTMX)
- Підтримує клавіатурну навігацію (←/→ для розмірів, ↑/↓ для кольорів)

---

## 4. Інтеграції

| Сервіс                           | Призначення                                 | Пріоритет     |
| -------------------------------- | ------------------------------------------- | ------------- |
| Нова Пошта API                   | Розрахунок доставки, відділення, ТТН        | MVP           |
| LiqPay / WayForPay               | Онлайн-оплата                               | MVP           |
| Google Tag Manager               | Аналітика і трекінг                         | MVP           |
| GA4 + Meta Pixel                 | Веб-аналітика                               | MVP           |
| Google Search Console + Indexing API | Швидкий індекс                          | MVP           |
| Telegram-бот                     | Сповіщення замовлень + бот для клієнта      | v1.1          |
| BinotelHub / Ringostat            | Колл-трекінг                               | v1.1          |
| Mailchimp / SendPulse            | Email-розсилки                              | v1.1          |
| Prom.ua / Rozetka XML feed        | Маркетплейси                               | v1.2          |
| Google Merchant + Performance Max | Google Shopping                            | v1.1          |

---

## 5. Чек-лист MVP (запуск)

### Блок 1 — Фундамент
- [ ] Django-проєкт ініціалізовано, settings розбито на base/dev/prod
- [ ] PostgreSQL + Redis у docker-compose
- [ ] requirements.txt з фіксацією версій
- [ ] Pre-commit (ruff, black, djlint)
- [ ] Базовий CI (тести, лінтери)

### Блок 2 — Каталог
- [ ] Моделі Section / Facet / ProductSeries / ProductVariant / ProductImage
- [ ] Адмінка з inlines, drag-and-drop сортуванням
- [ ] Імпорт перших 50-100 товарів (CSV/JSON management command)
- [ ] View головної з 12 топ-серіями
- [ ] View розділу
- [ ] View фасету з фільтром (HTMX, push-url)
- [ ] View картки серії з варіантами (swatch)

### Блок 3 — SEO
- [ ] BreadcrumbList JSON-LD на всіх сторінках
- [ ] Product / Organization / Article / FAQ JSON-LD у відповідних шаблонах
- [ ] Title/Description генератор (з override з адмінки)
- [ ] sitemap_index.xml + 4 саб-сайтмапи
- [ ] robots.txt
- [ ] Canonical і hreflang
- [ ] OpenGraph + Twitter Card
- [ ] Favicon + apple-touch-icon
- [ ] manifest.json (PWA-готовність)

### Блок 4 — Контент
- [ ] Блог: моделі + view + 3 перші статті
- [ ] FAQ-сторінка з FAQPage Schema
- [ ] Сторінки Доставка / Про нас / Контакти
- [ ] Відгуки: модель + блок на головній і на картці
- [ ] SEO-тексти на 5 кореневих розділах і ТОП-15 фасетах

### Блок 5 — Лідогенерація і покупка
- [ ] Кошик (cookie/session-based)
- [ ] Оформлення замовлення (Нова Пошта API: міста, відділення, поштомати)
- [ ] LiqPay/WayForPay для онлайн-оплати
- [ ] Форма "Замовити дзвінок" (модал)
- [ ] Форма "Допоможіть з вибором" (модал)
- [ ] Email-сповіщення адміна + клієнта
- [ ] Дякувальна сторінка з тригером покупки в GA4

### Блок 6 — UX/UI
- [ ] Header + Mega-menu (десктоп) + Drawer (моб.)
- [ ] Footer з 30 топ-фасетними посиланнями
- [ ] Sticky bottom CTA на картці товару (моб.)
- [ ] Pagination + "Більше товарів" (HTMX)
- [ ] iOS Safari фікси (safe-area, 100dvh, no-zoom, sticky без jitter)
- [ ] Calc для доріжок на відріз
- [ ] Темна / світла тема (опційно для v1.1)

### Блок 7 — Performance
- [ ] WebP конвертація + 3 розміри thumbnails
- [ ] Lazy loading + aspect-ratio
- [ ] Critical CSS inline для головної + категорій + картки
- [ ] Cache фасетних і серій сторінок у Redis
- [ ] Lighthouse ≥ 90 на 5 ключових сторінках
- [ ] CDN для static (опційно)

### Блок 8 — Аналітика
- [ ] GA4 + GTM
- [ ] Search Console + sitemap submitted
- [ ] Конверсійні події: переглянув_товар, додав_у_кошик, надіслав_лід, оформив_замовлення, дзвінок (через колл-трекер на v1.1)

### Блок 9 — Юр. і операційне
- [ ] Політика конфіденційності
- [ ] Умови повернення (30 днів)
- [ ] Договір публічної оферти
- [ ] Реквізити ФОП
- [ ] Страхування платежів LiqPay

---

## 6. Фішки, які виграють у конкурентів (резюме)

1. **Уніфікований мульти-фасет** — одна архітектура (kilimi не виграє в одному місці, dim-dim — лише по колекціях).
2. **Картка-серія + конструктор доріжки** — синтез сильних сторін обох конкурентів.
3. **HTMX-фільтр з push-state** — швидко як SPA, індексується як SSR.
4. **iOS Safari першочергово** — більшість конкурентів цього не роблять; ми — навпаки.
5. **Schema.org повний набір** — Product+Offer+Rating+Review+Breadcrumb+FAQ+Article+Organization.
6. **Контент-кластери** — 10 статей-pillar з in-text перелінковкою на категорії і товари.
7. **Калькулятор площі і "квіз 60 секунд"** — те, чого немає в конкурентів.
8. **Telegram/Viber бот для лідів поза робочим часом** — закриває втрату 50% звернень.
9. **Безкоштовна доставка від чіткого порогу** + повернення 30 днів — як у kilimi, але з прозорою комунікацією без невідповідностей (kilimi заявляє 800 на головній, 600 у FAQ).
10. **i18n із першого дня** — рос/англ як майбутні ринки + збереження SEO через hreflang.
11. **AR-перегляд через USDZ** на iPhone (опційно для v1.1) — wow-фактор без витрат на 3D-моделі (генерація з фото).

---

## 7. Залежності (попередній `requirements.txt`)

```
Django>=5.0,<6.0
django-environ
django-htmx
django-modeltranslation         # повна i18n полів моделі (опційно)
django-ratelimit
django-csp
django-imagekit                  # або Pillow + власний сигнал
django-debug-toolbar             # dev-only
django-extensions                # dev-only
django-admin-sortable2           # drag-and-drop сортування у адмінці
psycopg[binary]
redis
hiredis
gunicorn
whitenoise
python-slugify[unidecode]
beautifulsoup4                   # очистка rich-text
markdown                         # для статей блогу
requests                         # API НП, LiqPay
sentry-sdk[django]
pytest
pytest-django
pytest-cov
factory-boy
ruff
black
djlint
```

---

## 8. Наступні кроки після прочитання документа

1. **Погодити фінальну таксономію** (Розділ 2 у Частині 2). Якщо клієнт хоче інші назви/групи — зафіксувати тут.
2. **Створити Django-проєкт за структурою з Розділу 1 цієї частини**.
3. **Замоделювати ProductSeries / Variant / Facet** і налити перші 50 товарів (можна скрапінгом з конкурентів для тесту, потім свій каталог).
4. **Зробити Section + Facet view + базовий шаблон** із HTMX-фільтром.
5. **Закрити SEO-блок**: title-генератор, sitemap, schema.org, robots.
6. **Запустити MVP на test-домені**, прогнати Lighthouse + Search Console.
7. **Контент**: написати 3 перші статті блогу, заповнити FAQ, зібрати 10-15 відгуків.

---

> **Кінець документа.** Загальний обсяг: 4 файли, ~1500 рядків. Всі правила (≤500 рядків/файл, без `!important`, mobile-first, iOS-first, окремі CSS/JS/HTML) дотримані.
