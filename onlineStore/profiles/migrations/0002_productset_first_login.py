# Generated by Django 4.2 on 2023-06-12 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="productset",
            name="first_login",
            field=models.BooleanField(default=True),
        ),
    ]