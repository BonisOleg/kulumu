from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", _("Нове")
        CONFIRMED = "confirmed", _("Підтверджено")
        PAID = "paid", _("Оплачено")
        PROCESSING = "processing", _("Комплектується")
        SHIPPED = "shipped", _("Відправлено")
        DELIVERED = "delivered", _("Доставлено")
        CANCELLED = "cancelled", _("Скасовано")
        RETURNED = "returned", _("Повернуто")

    class DeliveryType(models.TextChoices):
        NP_WAREHOUSE = "np_warehouse", _("Нова Пошта — відділення")
        NP_POSTAMAT = "np_postamat", _("Нова Пошта — поштомат")
        NP_COURIER = "np_courier", _("Нова Пошта — адресна")

    class PaymentType(models.TextChoices):
        ONLINE = "online", _("Онлайн-оплата")
        COD = "cod", _("Накладений платіж (передоплата 20%)")

    # Контакти
    name = models.CharField(_("Ім'я"), max_length=100)
    phone = models.CharField(_("Телефон"), max_length=32)
    email = models.EmailField(_("Email"), blank=True)

    # Доставка
    delivery_type = models.CharField(
        _("Спосіб доставки"), max_length=20,
        choices=DeliveryType.choices, default=DeliveryType.NP_WAREHOUSE
    )
    np_city_ref = models.CharField(_("Ref міста НП"), max_length=40, blank=True)
    np_city_name = models.CharField(_("Місто"), max_length=100, blank=True)
    np_warehouse_ref = models.CharField(_("Ref відділення НП"), max_length=40, blank=True)
    np_warehouse_address = models.CharField(_("Відділення / адреса"), max_length=200, blank=True)

    # Оплата
    payment_type = models.CharField(
        _("Спосіб оплати"), max_length=20,
        choices=PaymentType.choices, default=PaymentType.ONLINE
    )
    payment_status = models.CharField(_("Статус оплати"), max_length=30, blank=True)
    payment_ref = models.CharField(_("Реф. оплати"), max_length=100, blank=True)

    # Статус
    status = models.CharField(
        _("Статус"), max_length=20,
        choices=Status.choices, default=Status.NEW, db_index=True
    )
    np_tracking_number = models.CharField(_("ТТН Нова Пошта"), max_length=30, blank=True)

    total_uah = models.PositiveIntegerField(_("Сума (грн)"), default=0)
    note = models.TextField(_("Примітка клієнта"), blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Замовлення")
        verbose_name_plural = _("Замовлення")
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} — {self.name} ({self.total_uah} ₴)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    series_name = models.CharField(_("Назва серії (знімок)"), max_length=120)
    variant_sku = models.CharField(_("SKU варіанту"), max_length=64)
    color_name = models.CharField(_("Колір"), max_length=60)
    size_display = models.CharField(_("Розмір"), max_length=30)
    quantity = models.PositiveSmallIntegerField(_("Кількість"), default=1)
    price_uah = models.PositiveIntegerField(_("Ціна за одиницю (грн)"))
    is_per_meter = models.BooleanField(_("На відріз"), default=False)
    length_m = models.DecimalField(_("Довжина (м)"), max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Позиція замовлення")
        verbose_name_plural = _("Позиції замовлення")

    def __str__(self):
        return f"{self.series_name} | {self.color_name} | {self.size_display}"

    @property
    def total(self):
        if not self.price_uah:
            return 0
        qty = float(self.length_m) if (self.is_per_meter and self.length_m) else (self.quantity or 1)
        return int(self.price_uah * qty)
