# Generated by Django 4.2.10 on 2024-03-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_product_on_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_sale',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='on_discount',
            field=models.BooleanField(default=False),
        ),
    ]
