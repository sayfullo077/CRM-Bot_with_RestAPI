# Generated by Django 4.2 on 2025-04-22 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=30,
                null=True,
                unique=True,
                verbose_name="phone number",
            ),
        ),
    ]
