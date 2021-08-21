from celery import signals
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .main import DataModels
from .tasks import handle_new_complaint, handle_new_complaint_detail


@receiver(post_save, sender=DataModels.Complaint)
def complaint_post_save(sender, **kwargs):
    if kwargs['created']:
        # handle_new_complaint().delay()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # https://github.com/celery/django-celery-results/issues/41
        transaction.on_commit(lambda: handle_new_complaint.delay())
        pass


@receiver(post_save, sender=DataModels.ComplaintDetail)
def complaint_detail_post_save(sender, **kwargs):
    # print('22222222222222')
    if kwargs['created']:
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # https://github.com/celery/django-celery-results/issues/41
        transaction.on_commit(lambda: handle_new_complaint_detail.delay())


@signals.task_retry.connect
@signals.task_failure.connect
@signals.task_revoked.connect
def on_task_failure(**kwargs):
    """Abort transaction on task errors.
    """
    # celery exceptions will not be published to `sys.excepthook`. therefore we have to create another handler here.
    import logging
    from traceback import format_tb

    logging.error('[task:%s:%s]' % (kwargs.get('task_id'), kwargs['sender'].request.correlation_id,)
                  + '\n'
                  + ''.join(format_tb(kwargs.get('traceback', [])))
                  + '\n'
                  + str(kwargs.get('exception', '')))
