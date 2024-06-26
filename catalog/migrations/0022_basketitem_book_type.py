# Generated by Django 4.2.7 on 2024-04-15 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0021_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="basketitem",
            name="book_type",
            field=models.CharField(
                choices=[("PB", "Paperback"), ("HB", "Hardback")],
                default="PB",
                max_length=2,
            ),
        ),
    ]
