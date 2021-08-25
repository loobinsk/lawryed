import os
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db.models import CharField, EmailField
from django.db.models.functions import Now
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models, connection

from django_extensions.db.models import TimeStampedModel
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = CharField(_("Full name"), blank=False, max_length=255)
    redirected_email = EmailField(_("Redirect all emails to"), blank=True)

    # TODO
    # company_name = CharField(_("Company name"), blank=False, default='', max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def company_get_file_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    res = os.path.join(f'user_company_{instance.user_id}', filename)
    return res


class Company(TimeStampedModel, models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    company_name = models.CharField(max_length=200, blank=False, verbose_name=_('The name of the company'), default='')
    owner_name = models.CharField(max_length=200, blank=False, verbose_name=_('The name of the company owner'))
    owner_surname = models.CharField(max_length=200, blank=False,
                                     verbose_name=_('Name and surname of the representative'))
    title = models.CharField(max_length=200, blank=False,
                             verbose_name=_('Position of the represenatative/position/title'))

    # address = models.CharField(max_length=200, blank=False,
    #                            verbose_name=_('Address of registration of the company owner'))
    address_country = CountryField(verbose_name=_('address country'))
    address_city = models.CharField(max_length=200, blank=False, verbose_name=_('City'))
    address_street = models.CharField(max_length=200, blank=False, verbose_name=_('Street Address'))
    address_state = models.CharField(max_length=200, blank=False, verbose_name=_('State/Province'))
    address_zip = models.CharField(max_length=200, blank=False, verbose_name=_('ZIP/Postal Code'))

    region = models.CharField(max_length=200, blank=True,
                              verbose_name=_('Region of registration of copyright, №, name TM'))
    # owner_date = models.CharField(max_length=200, blank=False, verbose_name=_('Date of commencement of business activities'))
    owner_date = models.DateField(blank=False, verbose_name=_('Date of commencement of business activities'))

    products = models.CharField(max_length=200, blank=False, verbose_name=_('Products that have been developed by'))

    email = models.EmailField(blank=False, verbose_name=_('Email represenatative'))

    additional = models.CharField(max_length=200, blank=False,
                                  verbose_name=_('EDRPOU code, HQ address, corporate phone number, corporate email address'),
                                  # help_text=_('Additional information about the company (EDRPOU code, HQ address, corporate phone number, '
                                  #             'corporate email address)')
                                  )
    additional2 = models.CharField(max_length=200, blank=False,
                                   verbose_name=_('Additional information about the object to be protected'))
    confirmation = models.CharField(max_length=200, blank=False, verbose_name=_('Confirmation of the acceptance of the user agreement'))
    website = models.URLField(max_length=200, blank=False, verbose_name=_('Company Website'))
    terms = models.URLField(max_length=200, blank=True, verbose_name=_('Terms'))

    phone = PhoneNumberField(blank=False, verbose_name=_('Representative telephone number'))
    youtube = models.URLField(max_length=200, blank=True, verbose_name=_('Link to the official Youtube channel'))

    document = models.FileField(upload_to=company_get_file_path, null=True, blank=False,
                                # validators=[validate_file_extension],
                                verbose_name=_('Confirmation of the possibility of representing interests'))

    document_right = models.FileField(upload_to=company_get_file_path, null=True, blank=False,
                                      verbose_name=_('Confirmation of rights to TM (PDF file with WIPO) '))

    # document = models.FileField(upload_to=assets_get_file_path, null=True, blank=True, help_text=_('document'))
    # status = models.IntegerField(choices=ASSETS_STATUS, default=ASSETS_STATUS.waiting, db_index=True, help_text=_('status'))

    # def get_absolute_url(self):
    #     return reverse('company', args=())

    @property
    def address(self):
        return f'{self.address_country.name}, {self.address_state}, {self.address_city}, {self.address_zip}, {self.address_street}'

    def __str__(self):
        return f'{self.id}-{self.user}-{self.title}'
