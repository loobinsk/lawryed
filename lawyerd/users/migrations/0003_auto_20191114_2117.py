# Generated by Django 2.2.3 on 2019-11-14 19:17

from django.db import migrations, models
import lawyerd.users.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_company_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='document_right',
            field=models.FileField(blank=True, null=True, upload_to=lawyerd.users.models.company_get_file_path, verbose_name='Confirmation of rights to TM (PDF file with WIPO) '),
        ),
        migrations.AlterField(
            model_name='company',
            name='additional',
            field=models.CharField(help_text='Additional information about the company (EDRPOU code, HQ address, corporate phone number, corporate email address)', max_length=200, verbose_name='Additional Information'),
        ),
        migrations.AlterField(
            model_name='company',
            name='additional2',
            field=models.CharField(max_length=200, verbose_name='Additional information about the object to be protected'),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Address of registration of the company owner'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(default='', max_length=200, verbose_name='The name of the company'),
        ),
        migrations.AlterField(
            model_name='company',
            name='confirmation',
            field=models.CharField(max_length=200, verbose_name='Confirmation of the acceptance of the user agreement'),
        ),
        migrations.AlterField(
            model_name='company',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=lawyerd.users.models.company_get_file_path, verbose_name='Confirmation of the possibility of representing interests'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email represenatative'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner_date',
            field=models.DateField(verbose_name='Date of commencement of business activities'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner_name',
            field=models.CharField(max_length=200, verbose_name='The name of the company owner'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner_surname',
            field=models.CharField(max_length=200, verbose_name='Name and surname of the representative'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Represenatative telephone number'),
        ),
        migrations.AlterField(
            model_name='company',
            name='products',
            field=models.CharField(max_length=200, verbose_name='Products that have been developed by'),
        ),
        migrations.AlterField(
            model_name='company',
            name='region',
            field=models.CharField(max_length=200, verbose_name='Region of registration of copyright, ???, name TM'),
        ),
        migrations.AlterField(
            model_name='company',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Position of the represenatative/position/title'),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.CharField(max_length=200, verbose_name='Company Website'),
        ),
        migrations.AlterField(
            model_name='company',
            name='youtube',
            field=models.URLField(blank=True, verbose_name='Link to the official Youtube channel'),
        ),
    ]
