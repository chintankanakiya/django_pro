# Generated by Django 3.1.6 on 2021-07-23 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='Prodect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
    ]
