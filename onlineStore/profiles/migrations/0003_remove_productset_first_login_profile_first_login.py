# Generated by Django 4.2 on 2023-06-12 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0002_productset_first_login"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productset",
            name="first_login",
        ),
        migrations.AddField(
            model_name="profile",
            name="first_login",
            field=models.BooleanField(default=True),
        ),
    ]
