"""
Management command: python manage.py seed_demo
Наповнює базу тестовими даними для демонстрації замовнику.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify


SECTIONS_DATA = [
    ("kylymy", "Килими", "kilymiv", "storefront"),
    ("dorizhky", "Доріжки", "dorіzh", "straighten"),
    ("kovrolin", "Ковролін", "kovrolinu", "layers"),
    ("dlya-vannoyi", "Килимки для ванної", "kilymkiv dlya vannoyi", "bathtub"),
    ("akciyi", "Акції", "akciynykh tovariv", "local_offer"),
]

FACETS_DATA = {
    "category": [
        ("vysokovorsni", "Високоворсні (Shaggy)"),
        ("nyzkovorsni", "Низьковорсні"),
        ("bezvorsovi", "Безворсові"),
        ("akrylovi", "Акрилові"),
        ("vovnyani", "Вовняні"),
        ("syntetychni", "Синтетичні"),
        ("na-gumoviy-osnovi", "На гумовій основі"),
        ("na-povstyaniy-osnovi", "На повстяній основі"),
    ],
    "purpose": [
        ("dlya-spalni", "У спальню"),
        ("dlya-vitalni", "У вітальню"),
        ("dlya-kuhni", "На кухню"),
        ("dlya-dytyachoyi", "У дитячу"),
        ("dlya-prykhozhoyi", "У прихожу"),
        ("dlya-koridoru", "У коридор"),
        ("dlya-ofisu", "Для офісу"),
        ("prydverni", "Придверні"),
    ],
    "style": [
        ("suchasni", "Сучасні"),
        ("klasychni", "Класичні"),
        ("skhidni", "Східні"),
        ("dytyachi", "Дитячі"),
        ("odnotonni", "Однотонні"),
        ("geometriya", "Геометрія"),
    ],
    "form": [
        ("pryamokutni", "Прямокутні"),
        ("ovalni", "Овальні"),
        ("kruhli", "Круглі"),
        ("kvadratni", "Квадратні"),
    ],
    "size": [
        ("0.8x1.5", "0.8×1.5 м"),
        ("1.2x1.8", "1.2×1.8 м"),
        ("1.6x2.3", "1.6×2.3 м"),
        ("2.0x3.0", "2.0×3.0 м"),
        ("2.4x3.4", "2.4×3.4 м"),
        ("3.0x4.0", "3.0×4.0 м"),
    ],
    "color": [
        ("siryi", "Сірий", "#808080"),
        ("bezhevyi", "Бежевий", "#d4b896"),
        ("korychnnevyi", "Коричневий", "#7b4d2e"),
        ("chornyi", "Чорний", "#1a1a1a"),
        ("bilyi", "Білий", "#f5f5f0"),
        ("blakytyi", "Блакитний", "#5b9bd5"),
        ("zelenyi", "Зелений", "#4f8a4a"),
        ("ryvyi", "Рожевий", "#e8a0b0"),
    ],
    "manufacturer": [
        ("turechchyna", "Туреччина"),
        ("belghiya", "Бельгія"),
        ("ukrayina", "Україна"),
        ("moldova", "Молдова"),
        ("polshcha", "Польща"),
    ],
}

SERIES_DATA = [
    {
        "name": "Shaggy Roco",
        "section_slug": "kylymy",
        "facet_slugs": ["vysokovorsni", "suchasni", "dlya-spalni", "pryamokutni", "turechchyna"],
        "composition": "Поліпропілен 100%",
        "pile_height_mm": 50,
        "country": "Туреччина",
        "is_top": True,
        "is_new": True,
        "short_descr": "Мʼякий та густий ворс Shaggy Roco створює відчуття розкоші у вашій спальні або вітальні.",
        "variants": [
            {"sku": "SR-GREY-080150", "color": "siryi", "width_cm": 80, "length_cm": 150, "price_uah": 1804},
            {"sku": "SR-GREY-160230", "color": "siryi", "width_cm": 160, "length_cm": 230, "price_uah": 5016},
            {"sku": "SR-GREY-200300", "color": "siryi", "width_cm": 200, "length_cm": 300, "price_uah": 8712},
            {"sku": "SR-BEIGE-080150", "color": "bezhevyi", "width_cm": 80, "length_cm": 150, "price_uah": 1804},
            {"sku": "SR-BEIGE-200300", "color": "bezhevyi", "width_cm": 200, "length_cm": 300, "price_uah": 8712},
        ],
    },
    {
        "name": "Espresso Classic",
        "section_slug": "kylymy",
        "facet_slugs": ["nyzkovorsni", "klasychni", "dlya-vitalni", "pryamokutni", "turechchyna"],
        "composition": "Поліпропілен 100%",
        "pile_height_mm": 8,
        "country": "Туреччина",
        "is_top": True,
        "short_descr": "Щільний короткий ворс — ідеально для вітальні з великим навантаженням.",
        "variants": [
            {"sku": "EC-GREY-080150", "color": "siryi", "width_cm": 80, "length_cm": 150, "price_uah": 780, "old_price_uah": 850},
            {"sku": "EC-GREY-120180", "color": "siryi", "width_cm": 120, "length_cm": 180, "price_uah": 1400, "old_price_uah": 1500},
            {"sku": "EC-GREY-160230", "color": "siryi", "width_cm": 160, "length_cm": 230, "price_uah": 2300},
            {"sku": "EC-GREY-200300", "color": "siryi", "width_cm": 200, "length_cm": 300, "price_uah": 3900, "old_price_uah": 4100},
            {"sku": "EC-BEIGE-080150", "color": "bezhevyi", "width_cm": 80, "length_cm": 150, "price_uah": 780},
            {"sku": "EC-BEIGE-200300", "color": "bezhevyi", "width_cm": 200, "length_cm": 300, "price_uah": 3900},
        ],
        "discount_percent": 5,
    },
    {
        "name": "Kids Fun City",
        "section_slug": "kylymy",
        "facet_slugs": ["syntetychni", "dytyachi", "dlya-dytyachoyi", "pryamokutni", "belghiya"],
        "composition": "Поліестер 100%",
        "pile_height_mm": 10,
        "country": "Бельгія",
        "is_new": True,
        "short_descr": "Яскравий дитячий килим з картою міста — сприяє навчанню та грі.",
        "variants": [
            {"sku": "KFC-MULTI-080150", "color": "zelenyi", "width_cm": 80, "length_cm": 150, "price_uah": 1364},
            {"sku": "KFC-MULTI-120170", "color": "zelenyi", "width_cm": 120, "length_cm": 170, "price_uah": 2068},
            {"sku": "KFC-MULTI-160230", "color": "zelenyi", "width_cm": 160, "length_cm": 230, "price_uah": 3476},
        ],
    },
]


class Command(BaseCommand):
    help = "Заповнити базу демо-даними для презентації"

    def handle(self, *args, **options):
        from apps.catalog.models import Facet, FacetType, Section, ProductSeries, ProductVariant

        self.stdout.write("🌱 Запускаємо seed_demo...")

        # Sections
        for slug, name, genitive, icon in SECTIONS_DATA:
            section, created = Section.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "name_genitive": genitive,
                    "icon_name": icon,
                    "sort_order": SECTIONS_DATA.index((slug, name, genitive, icon)),
                },
            )
            if created:
                self.stdout.write(f"  + Розділ: {name}")

        # Facets
        sort_counter = {}
        for facet_type, items in FACETS_DATA.items():
            sort_counter[facet_type] = 0
            for item in items:
                slug, name = item[0], item[1]
                color_hex = item[2] if len(item) > 2 else ""
                sort_counter[facet_type] += 10
                facet, created = Facet.objects.get_or_create(
                    type=facet_type,
                    slug=slug,
                    defaults={
                        "name": name,
                        "color_hex": color_hex,
                        "sort_order": sort_counter[facet_type],
                    },
                )
                if created:
                    self.stdout.write(f"  + Фасет [{facet_type}]: {name}")

        # Series + Variants
        for data in SERIES_DATA:
            section = Section.objects.get(slug=data["section_slug"])
            slug = slugify(data["name"], allow_unicode=False).replace(" ", "-")
            series, created = ProductSeries.objects.get_or_create(
                section=section,
                slug=slug,
                defaults={
                    "name": data["name"],
                    "short_descr": data.get("short_descr", ""),
                    "composition": data.get("composition", ""),
                    "pile_height_mm": data.get("pile_height_mm"),
                    "country": data.get("country", ""),
                    "is_top": data.get("is_top", False),
                    "is_new": data.get("is_new", False),
                    "discount_percent": data.get("discount_percent", 0),
                    "is_active": True,
                },
            )
            if created:
                facets = Facet.objects.filter(slug__in=data.get("facet_slugs", []))
                series.facets.set(facets)
                self.stdout.write(f"  + Серія: {data['name']}")

            for vdata in data.get("variants", []):
                color = Facet.objects.filter(type="color", slug=vdata["color"]).first()
                if not color:
                    continue
                ProductVariant.objects.get_or_create(
                    sku=vdata["sku"],
                    defaults={
                        "series": series,
                        "color": color,
                        "width_cm": vdata["width_cm"],
                        "length_cm": vdata.get("length_cm"),
                        "price_uah": vdata["price_uah"],
                        "old_price_uah": vdata.get("old_price_uah"),
                        "in_stock": True,
                        "ready_to_ship": True,
                    },
                )

        # SiteSettings
        from apps.core.models import SiteSettings
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "phone": "+380631234567",
                "phone_display": "+380 (63) 123-45-67",
                "work_hours": "Пн–Пт 9:00–19:00, Сб 10:00–18:00",
                "email": "info@kylymy.ua",
                "instagram_url": "https://instagram.com/kylymy",
                "free_delivery_threshold": 1500,
                "delivery_price": 70,
                "return_days": 30,
            },
        )

        self.stdout.write(self.style.SUCCESS("✅ seed_demo завершено!"))
