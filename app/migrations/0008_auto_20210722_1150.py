# Generated by Django 3.1.6 on 2021-07-22 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_delete_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_image',
            field=models.ImageField(default=2, upload_to='img'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='p_price',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
