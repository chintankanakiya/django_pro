# Generated by Django 3.1.6 on 2021-07-29 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='qyantity',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]