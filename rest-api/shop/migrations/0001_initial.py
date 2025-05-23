# Generated by Django 4.2 on 2025-04-26 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title_uz", models.CharField(blank=True, max_length=255, null=True)),
                ("title_en", models.CharField(blank=True, max_length=255, null=True)),
                ("title_uk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ru", models.CharField(blank=True, max_length=255, null=True)),
                ("desc_uz", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_en", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_uk", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_ru", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "image",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.media",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Shop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title_uz", models.CharField(blank=True, max_length=255, null=True)),
                ("title_en", models.CharField(blank=True, max_length=255, null=True)),
                ("title_uk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ru", models.CharField(blank=True, max_length=255, null=True)),
                ("desc_uz", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_en", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_uk", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_ru", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "url",
                    models.URLField(validators=[shop.validators.validate_telegram_url]),
                ),
                (
                    "image",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.media",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Shop",
                "verbose_name_plural": "Shops",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title_uz", models.CharField(blank=True, max_length=255, null=True)),
                ("title_en", models.CharField(blank=True, max_length=255, null=True)),
                ("title_uk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ru", models.CharField(blank=True, max_length=255, null=True)),
                ("desc_uz", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_en", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_uk", models.CharField(blank=True, max_length=500, null=True)),
                ("desc_ru", models.CharField(blank=True, max_length=500, null=True)),
                ("price", models.BigIntegerField(default=0)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.category"
                    ),
                ),
                (
                    "image",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.media",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.AddField(
            model_name="category",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shop.shop"
            ),
        ),
    ]
