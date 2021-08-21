# Generated by Django 2.2.7 on 2021-02-23 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20191121_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='itype',
            field=models.IntegerField(choices=[(0, 'game'), (1, 'software'), (2, 'photo'), (3, 'picture'), (4, 'course')], db_index=True, default=0, help_text='product type', verbose_name='Type of product'),
        ),
    ]
