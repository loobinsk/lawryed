import os
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models  # , connection
# from django.db.models import Q, Index
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

PRODUCT_STATUS = Choices(
    (0, 'waiting', _('waiting')),
    (1, 'accepted', _('accepted')),
    # (2, 'complete', _('complete')),
    (3, 'cancelled', _('cancelled')),
    # (4, 'stopped', _('stopped')),
)

PRODUCT_TYPE = Choices(
    (0, 'game', _('Game')),
    (1, 'software', _('Software')),
    (2, 'photo', _('Photo')),
    (3, 'picture', _('Picture')),
    (4, 'course', _('Course')),
    (5, 'brand', _('Brand')),
)


def validate_product_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def product_get_file_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    res = os.path.join(f'user_product_{instance.user_id}', filename)
    return res


class Product(TimeStampedModel, models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, verbose_name=_('The name of the product'))
    document = models.FileField(upload_to=product_get_file_path, null=True, blank=False,
                                validators=[validate_product_file_extension],
                                verbose_name=_(
                                    'Proof of product rights (Trademark from Global Brand Database or national registers)'))  # noqa
    document_file_name = models.CharField(max_length=200, blank=False, verbose_name=_('Document file name'))
    status = models.IntegerField(choices=PRODUCT_STATUS, blank=False, default=PRODUCT_STATUS.waiting, db_index=True,
                                 help_text=_('status'))
    itype = models.IntegerField(choices=PRODUCT_TYPE, blank=False, default=PRODUCT_TYPE.game, db_index=True,
                                verbose_name=_('Type of product'))

    def __str__(self):
        return f'{self.id}-{self.user}-{self.document}'
