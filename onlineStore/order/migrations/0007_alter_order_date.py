# Generated by Django 4.2 on 2023-06-15 09:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0006_alter_order_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateField(default=datetime.date(2023, 6, 15)),
        ),
    ]
