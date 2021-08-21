from typing import List

from config.celery_app import app
from .main import DataModels, get_sites_list, BackendStorage, Poster  # PosterBackend, Poster


@app.task
def handle_new_complaint():
    print('New complaint_work...')
    complaint: DataModels.Complaint = DataModels.Complaint.get_new()
    if not complaint:
        return None
    print(f'Start Complaint: {complaint.id} in process...')
    sites_list: List = get_sites_list(complaint.search_text, complaint.product.name, complaint.site_count)

    # Be aware bulk_create() does NOT call a model's save() method; and thus the `pre_save` and `post_save` signals will not be sent.
    # This may or may not be an issue for your scenario.
    DataModels.ComplaintDetail.objects.bulk_create(
        [DataModels.ComplaintDetail(
            complaint=complaint,
            site=url,
            status=DataModels.STATUS.waiting
        ) for url in sites_list]
    )

    # just run workers
    for site in sites_list:  # noqa
        handle_new_complaint_detail()

    # complaint.finished = Now()
    # complaint.save()
    s = f'End complaint work, created: {len(sites_list)} details records'
    print(s)
    # return s


@app.task
def handle_new_complaint_detail():
    complaint_detail: DataModels.ComplaintDetail = DataModels.ComplaintDetail.get_new()
    if not complaint_detail:
        return None

    backend: Poster = BackendStorage.get_url_backend(complaint_detail.site)
    x: Poster = backend(complaint_detail)  # noqa
    x.execute()
    pass


# # @app.task
# def handle_save_complaint_status(complaint_detail: DataModels.ComplaintDetail):
#     DataModels.Complaint.objects.filter(id=complaint_detail.id)
#     pass
