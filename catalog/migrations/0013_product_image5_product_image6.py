# Generated by Django 4.2.7 on 2024-04-06 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0012_rename_catalog_purchase_catalogpurchase_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image5",
            field=models.ImageField(
                default="products/default.jpg", upload_to="products/"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="image6",
            field=models.ImageField(
                default="products/default.jpg", upload_to="products/"
            ),
        ),
    ]