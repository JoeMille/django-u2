# Generated by Django 4.2.7 on 2024-04-15 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0020_remove_orderitem_item_orderitem_product_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                ("house_number", models.CharField(max_length=255)),
                ("street_name", models.CharField(max_length=255)),
                ("town_city", models.CharField(max_length=255)),
                ("county", models.CharField(max_length=255)),
                ("eir_code", models.CharField(max_length=7)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
