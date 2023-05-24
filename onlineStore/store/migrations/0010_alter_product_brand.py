# Generated by Django 4.2 on 2023-05-24 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0009_alter_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.CharField(
                choices=[
                    ("Apple", "Apple"),
                    ("Samsung", "Samsung"),
                    ("OPPO", "OPPO"),
                    ("Huawei", "Huawei"),
                    ("Microsoft", "Microsoft"),
                    ("Infinix", "Infinix"),
                    ("HP", "HP"),
                ],
                max_length=100,
            ),
        ),
    ]
