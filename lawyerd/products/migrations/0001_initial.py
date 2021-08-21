# Generated by Django 2.2.3 on 2019-11-07 00:22

from django.db import migrations, models
import django_extensions.db.fields
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(help_text='The name of the products', max_length=200)),
                ('document', models.FileField(blank=True, help_text='Confirmation of the rights to TM (PDF  file with WIPO)', null=True, upload_to=products.models.product_get_file_path, validators=[products.models.validate_product_file_extension])),
                ('document_file_name', models.CharField(help_text='Document file name', max_length=200)),
                ('status', models.IntegerField(choices=[(0, 'waiting'), (1, 'accepted'), (3, 'cancelled')], db_index=True, default=0, help_text='status')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]