# Generated by Django 4.2.7 on 2024-04-11 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0015_sale"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("name", models.CharField(default="Default Name", max_length=255)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("house", models.CharField(default="Default House", max_length=255)),
                ("street", models.CharField(default="Default Street", max_length=255)),
                ("city", models.CharField(default="Default City", max_length=255)),
                ("county", models.CharField(default="Default County", max_length=255)),
                ("eircode", models.CharField(default="0000000", max_length=7)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("credit_card", "Credit Card"),
                            ("debit_card", "Debit Card"),
                            ("paypal", "PayPal"),
                        ],
                        default="credit_card",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("order_items", models.ManyToManyField(to="catalog.item")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="catalog_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompletedOrder",
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
                ("order_items", models.TextField()),
                ("address", models.CharField(max_length=255)),
                ("payment_type", models.CharField(max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="completed_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
