# Generated by Django 4.2 on 2023-05-04 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_profile_cart_alter_profile_favourites'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(default='1_1', max_length=10),
            preserve_default=False,
        ),
    ]
