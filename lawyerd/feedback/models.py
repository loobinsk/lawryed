import os
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models  # , connection
# from django.db.models import Q, Index
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class Feedback(TimeStampedModel, models.Model):
    name = models.CharField(max_length=200, blank=False, verbose_name=_('Name'))
    email = models.CharField(max_length=200, blank=False, verbose_name=_('Email'))
    phone = models.CharField(max_length=200, blank=False, verbose_name=_('Phone'))

    def __str__(self):
        return f'{self.id}-{self.name}-{self.email}-{self.phone}'
