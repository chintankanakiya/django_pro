# Generated by Django 3.1.6 on 2021-07-22 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_price',
            field=models.IntegerField(max_length=10, null=True),
        ),
    ]
