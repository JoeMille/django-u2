# Generated by Django 4.2.7 on 2024-04-05 19:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0011_rename_purchase_catalog_purchase"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="catalog_purchase",
            new_name="CatalogPurchase",
        ),
        migrations.RemoveField(
            model_name="product",
            name="second_description",
        ),
        migrations.AddField(
            model_name="product",
            name="description2",
            field=models.TextField(default="Default Description"),
        ),
        migrations.AddField(
            model_name="product",
            name="image2",
            field=models.ImageField(
                default="products/default.jpg", upload_to="products/"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="image3",
            field=models.ImageField(
                default="products/default.jpg", upload_to="products/"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="image4",
            field=models.ImageField(
                default="products/default.jpg", upload_to="products/"
            ),
        ),
    ]
