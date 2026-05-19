import io
import logging
import os

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from slugify import slugify

from .models.media import ProductImage
from .models.series import ProductSeries

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=ProductSeries)
def auto_generate_slug(sender, instance, **kwargs):
    """Генерує slug з назви якщо не задано вручну."""
    if not instance.slug and instance.name:
        base_slug = slugify(instance.name, allow_unicode=False)
        slug = base_slug
        counter = 1
        qs = ProductSeries.objects.filter(section=instance.section)
        if instance.pk:
            qs = qs.exclude(pk=instance.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug


@receiver(post_save, sender=ProductImage)
def generate_thumbnails(sender, instance, created, **kwargs):
    """Після збереження зображення генерує WebP та мініатюру через Pillow."""
    if not instance.image:
        return
    if instance.image_webp and instance.image_thumb:
        return

    try:
        from PIL import Image

        img_path = instance.image.path
        if not os.path.exists(img_path):
            return

        with Image.open(img_path) as img:
            img = img.convert("RGB")

            # WebP 800px
            webp_buf = io.BytesIO()
            img_resized = img.copy()
            img_resized.thumbnail((800, 800), Image.LANCZOS)
            img_resized.save(webp_buf, format="WEBP", quality=85)
            webp_name = f"products/webp/{instance.series.slug}_{instance.pk}.webp"

            # Мініатюра 400px
            thumb_buf = io.BytesIO()
            img_thumb = img.copy()
            img_thumb.thumbnail((400, 400), Image.LANCZOS)
            img_thumb.save(thumb_buf, format="WEBP", quality=80)
            thumb_name = f"products/thumb/{instance.series.slug}_{instance.pk}.webp"

            from django.core.files.base import ContentFile

            webp_buf.seek(0)
            thumb_buf.seek(0)

            # Зберігаємо без повторного запуску сигналу
            ProductImage.objects.filter(pk=instance.pk).update(
                image_webp=ContentFile(webp_buf.read(), name=os.path.basename(webp_name)),
                image_thumb=ContentFile(thumb_buf.read(), name=os.path.basename(thumb_name)),
            )
    except Exception:
        logger.exception("generate_thumbnails failed for ProductImage pk=%s", instance.pk)
