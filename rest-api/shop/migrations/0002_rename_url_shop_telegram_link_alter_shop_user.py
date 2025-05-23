# Generated by Django 4.2 on 2025-04-28 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shop",
            old_name="url",
            new_name="telegram_link",
        ),
        migrations.AlterField(
            model_name="shop",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shops",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
