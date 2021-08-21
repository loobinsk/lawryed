from django.urls import path

from api.v1.views import ComplaintList, ComplaintAdd, ComplaintSetStatus, ComplaintDetailList, \
    ProductView, ProductDelete, AnonymousSearch

# GetSiteScreenshot, GetSitesList, GetSiteHosting, GetSiteHostingAbuseEmail

app_name = "api"
urlpatterns = [
    path('anonymous_search_view/', AnonymousSearch.as_view(), name='anonymous_sarch'),

    path('complaint_list/', ComplaintList.as_view({'get': 'list'}), name='complaint_list'),
    path('complaint_add/', ComplaintAdd.as_view(), name='complaint_add'),
    path('complaint_setstatus/', ComplaintSetStatus.as_view(), name='complaint_cancel'),

    path('complaint_details_list/', ComplaintDetailList.as_view({'get': 'list'}), name='complaint_details_list'),

    path('product_view/', ProductView.as_view({'get': 'list'}), name='product_list'),
    path('product_delete/', ProductDelete.as_view(), name='product_delete'),

    # internal
    # path('get_sites_list/', GetSitesList.as_view(), name='get_sites_list'),
    # path('get_site_screenshot/', GetSiteScreenshot.as_view(), name='get_site_screenshot'),
    # path('get_site_hosting/', GetSiteHosting.as_view(), name='get_site_hosting'),
    # path('get_site_hosting_abuse_email/', GetSiteHostingAbuseEmail.as_view(), name='get_site_hosting_abuse_email'),
]
