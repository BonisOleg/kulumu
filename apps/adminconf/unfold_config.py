from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Kylymy",
    "SITE_HEADER": "Kylymy Admin",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("admin/logo.svg"),
        "dark": lambda request: static("admin/logo.svg"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("admin/logo.svg"),
        "dark": lambda request: static("admin/logo.svg"),
    },
    "SITE_SYMBOL": "storefront",
    "DASHBOARD_CALLBACK": "apps.adminconf.views.dashboard_callback",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "STYLES": [],
    "SCRIPTS": [],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "255 247 237",
            "100": "255 237 213",
            "200": "254 215 170",
            "300": "253 186 116",
            "400": "251 146 60",
            "500": "180 138 94",
            "600": "157 114 72",
            "700": "124 85 50",
            "800": "100 65 35",
            "900": "78 48 24",
            "950": "59 33 15",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uk": "🇺🇦",
                "en": "🇬🇧",
            }
        }
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Каталог"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Серії товарів"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:catalog_productseries_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Варіанти"),
                        "icon": "format_size",
                        "link": reverse_lazy("admin:catalog_productvariant_changelist"),
                    },
                    {
                        "title": _("Розділи"),
                        "icon": "category",
                        "link": reverse_lazy("admin:catalog_section_changelist"),
                    },
                    {
                        "title": _("Фасети"),
                        "icon": "filter_list",
                        "link": reverse_lazy("admin:catalog_facet_changelist"),
                    },
                ],
            },
            {
                "title": _("Замовлення"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Замовлення"),
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:cart_order_changelist"),
                        "badge": "apps.adminconf.badges.new_orders_count",
                    },
                    {
                        "title": _("Ліди / Дзвінки"),
                        "icon": "phone_in_talk",
                        "link": reverse_lazy("admin:leads_callbackrequest_changelist"),
                        "badge": "apps.adminconf.badges.pending_leads_count",
                    },
                ],
            },
            {
                "title": _("Контент"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Статті"),
                        "icon": "article",
                        "link": reverse_lazy("admin:content_article_changelist"),
                    },
                    {
                        "title": _("FAQ"),
                        "icon": "help_outline",
                        "link": reverse_lazy("admin:content_faqitem_changelist"),
                    },
                    {
                        "title": _("Відгуки"),
                        "icon": "rate_review",
                        "link": reverse_lazy("admin:reviews_review_changelist"),
                        "badge": "apps.adminconf.badges.pending_reviews_count",
                    },
                    {
                        "title": _("Сторінки"),
                        "icon": "description",
                        "link": reverse_lazy("admin:content_staticpage_changelist"),
                    },
                ],
            },
            {
                "title": _("Налаштування"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Сайт"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                    },
                    {
                        "title": _("Користувачі"),
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
        ],
    },
}
