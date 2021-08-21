import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, IntegerField
from django.db.models.expressions import Window, Case, When, Value
from django.db.models.functions import RowNumber
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from model_utils import Choices

from lawyerd.users.models import Company
from products.models import Product


# requests.packages.urllib3.disable_warnings()

# share status for Complaint and ComplaintDetail
STATUS = Choices(
    (0, 'waiting', _('waiting')),
    (1, 'processing', _('processing')),
    (2, 'ok', _('ok')),
    (3, 'cancelled', _('cancelled')),
    # (4, 'stopped', _('stopped')), ???
    (5, 'error', _('error')),
)

# need for calculate status in complaint from details
COMPLAINT_STATUS_FROM_DETAILS_MAP = {
    # key: priority
    STATUS.waiting: 1,
    STATUS.processing: 0,
    STATUS.ok: 4,
    STATUS.cancelled: 2,
    STATUS.error: 3,
}

# just helper function
REVERSED_COMPLAINT_STATUS_FROM_DETAILS_MAP = {value: key for key, value in COMPLAINT_STATUS_FROM_DETAILS_MAP.items()}


# region 'Complaint'


class Complaint(TimeStampedModel, models.Model):
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE, help_text=_("User"))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, help_text=_("Product"))
    search_text = models.CharField(max_length=1000, null=False, default='', help_text=_("Search text"))
    email = models.EmailField(null=True, default='', help_text=_("Email to send abuse"))
    site_count = models.PositiveIntegerField(
        null=False, default=1, validators=[MinValueValidator(1), ], help_text=_("Count"))
    status = models.IntegerField(choices=STATUS, default=STATUS.waiting, db_index=True, help_text=_("Status"))
    finished = models.DateTimeField(null=True, help_text=_('Finish task Datetime '))

    class Meta:
        db_table = 'complaints'

    def __str__(self):
        return f'{self.user.email}, {self.email}, text: {self.search_text}, status: {STATUS[self.status]}'  # noqa

    def status_value(self):  # noqa
        # TODO: rework to ORM
        # additional field for status (percent of execute, etc...)
        res = STATUS.waiting

        # qs = Order.get_active()
        # for item in qs:
        #     if self.id == item['id']:
        #         res = item['row_number']
        #         break

        # res = Complaint.get_status(self)

        return res

    @staticmethod
    def get_active(status=STATUS.waiting):
        qs = Complaint.objects.filter(status=status, user__is_active=True).annotate(row_number=Window(
            expression=RowNumber(),
            # partition_by=[F('created')],
            order_by=F('created').asc()
        )
        ).order_by('-created')

        return qs

    @staticmethod
    def get_active_count():
        return len(Complaint.get_active())

    @staticmethod
    def get_new(status: STATUS = STATUS.waiting, change_status: STATUS = STATUS.processing):
        res: Complaint
        # obj: Complaint = Complaint.objects.clear_ordering()  # filter(status=status).order_by('-created').first()

        # with transaction.atomic():

        complaint: Complaint = Complaint.get_active(status).order_by('created').first()
        # print(f'!!!!!!!!!!!! { obj.query}')
        if not complaint:
            return None

        if change_status:
            complaint.status = change_status
            complaint.save()
        # .order('-date')
        res = complaint

        return res


# endregion

# region 'ComplaintDetail'
def complaint_details_get_file_path(instance, filename) -> str:  # noqa
    ext = filename.split('.')[-1].lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    # res = os.path.join(f'order_screenshot_user_{instance.user_id}', filename)
    res = os.path.join(f'complaint_id_{instance.complaint_id}', filename)
    return res


class ComplaintDetail(TimeStampedModel, models.Model):
    complaint = models.ForeignKey(to=Complaint, on_delete=models.CASCADE, help_text=_("Complaint"))
    site = models.CharField(max_length=1000, null=True, help_text=_("Complaint URL"))
    hosting = models.CharField(max_length=255, null=True, help_text=_("Complaint hosting"))
    email = models.EmailField(max_length=255, null=True, help_text=_("Email"))
    screenshot = models.ImageField(
        upload_to=complaint_details_get_file_path, null=True, blank=True, help_text=_("Screenshot"))
    status = models.SmallIntegerField(choices=STATUS, default=STATUS.waiting, db_index=True, help_text=_("Status"))
    template_name = models.CharField(max_length=255, null=True, help_text=_("Template name"))

    class Meta:
        db_table = 'complaint_details'

    @staticmethod
    def get_active(status: STATUS = STATUS.waiting):
        qs = ComplaintDetail.objects.filter(status=status, complaint__user__is_active=True).annotate(
            row_number=Window(expression=RowNumber(),
                # partition_by=[F('created')],
                order_by=F('created').asc()
            )
        ).order_by('-created')

        return qs

    @staticmethod
    def get_new(status: STATUS = STATUS.waiting):
        res: ComplaintDetail

        # get complaint in process
        complaint = Complaint.get_new(STATUS.processing, None)
        if not complaint:
            return None

        complaint_details = ComplaintDetail.get_active(status=status).first()
        if not complaint_details:
            return None

        res = complaint_details
        return res

    @staticmethod
    def get_status(complaint_id):
        res = STATUS.ok

        # calculate count every status of complaint details
        case_conditions = [When(status=x, then=Value(y)) for x, y in COMPLAINT_STATUS_FROM_DETAILS_MAP.items()]

        qs = ComplaintDetail.objects.filter(complaint_id=complaint_id) \
            .annotate(status_index=Case(*case_conditions, output_field=IntegerField())) \
            .order_by('status_index') \
            .first()

        if qs:
            res = REVERSED_COMPLAINT_STATUS_FROM_DETAILS_MAP[qs.status_index]

        return res

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # set final status if all tasks complete
        status = ComplaintDetail.get_status(complaint_id=self.complaint_id)

        print(status)
        if status not in [STATUS.waiting, STATUS.processing]:
            complaint = Complaint.objects.filter(id=self.complaint_id).first()
            complaint.status = status
            complaint.save()

        pass
# endregion
