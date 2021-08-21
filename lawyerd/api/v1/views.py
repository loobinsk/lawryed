# api/views.py
import hashlib
from random import randrange

from django.db.models import Value, Sum, IntegerField, Window, Count
from django.http import HttpResponse
from django.db.models import CharField, Value

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from rest_framework.views import APIView
from rest_framework.response import Response

from api.v1.serializers import ComplaintSerializer, ComplaintSetStatusSerializer, ProductSerializer, \
    ComplaintDetailsSerializer, \
    SiteScreenshotSerializer, GetSitesListSerializer, SiteHostingAbuseEmailSerializer, SiteHostingSerializer

from complaint.models import Complaint, ComplaintDetail, STATUS
# get_sites_list, \
# get_site_hosting, \
# get_site_hosting_abuse_email, get_site_screenshot
from products.models import Product, PRODUCT_STATUS
from project.views import validate_oops_page
from config.settings.base import API_KEY_INTERNAL
from config.celery_app import app


@permission_classes([IsAuthenticated])
class ComplaintList(ModelViewSet):
    """
    Get site Orders
    """

    serializer_class = ComplaintSerializer

    def get_queryset(self, ):
        qs = Complaint.objects.filter(user=self.request.user) \
            .annotate(status_value=Value(STATUS.waiting, output_field=IntegerField())) \
            .values('id',
                    'created',
                    'modified',
                    'product__name',
                    'search_text',
                    # 'email',
                    # 'site_count',
                    'status',
                    'status_value',
                    )
        return qs


# from celery.task import Task
#
#
# class MyTask(Task):
#     name = "myapp.mytask"
#
#     def run(self, x, y):
#         return x * y


@permission_classes([IsAuthenticated])
class ComplaintAdd(generics.GenericAPIView):
    """
    Add Order
    """

    serializer_class = ComplaintSerializer

    # serializer_class = ComplaintAddSerializer

    def post(self, request, *args, **kwargs):
        # add2().delay()
        # MyTask.delay(2, 2)
        # return Response('{}')
        ##########################

        # check if need oops page
        res = validate_oops_page(request)

        # nned show oopspage
        if res['show_oops_page']:
            return Response(res)

        # send_to_email = self.request.data['email'] if self.request.user.is_superuser else ''
        # oops_page = False
        site_count = 20
        search_text = self.request.data['search_text'].strip()

        product_id = int(self.request.data['product_id'])
        product = Product.objects.filter(user=self.request.user, status__in=[PRODUCT_STATUS.accepted],
                                         id=product_id).first()

        # not enter search text or selected product
        if not (search_text or product):
            return Response()

        # error_handler('dffghfgh')

        # all fine, WORK !
        complaint_object = Complaint.objects.create(
            user=self.request.user,
            search_text=search_text,
            product=product,
            site_count=site_count,
        )

        res = {
            'oops_page': False,
            'search_results': 1,
        }

        return Response(res)


@app.task(bind=True)
def add2(self):
    print('fghfghfgh')
    return 77


# @app.task()
# def error_handler(uuid):
#     result = uuid
#
#     print('Task {0} raised exception: {1!r}\n{2!r}'.format(
#           uuid, 'exc', result.traceback))


@permission_classes([IsAuthenticated])
class ComplaintDetailList(ModelViewSet):
    """
    Get order details
    """

    serializer_class = ComplaintDetailsSerializer

    def get_queryset(self, ):
        qs = ComplaintDetail.objects.filter(complaint__user=self.request.user)
        if self.request.query_params["complaint_id"]:
            qs = qs.filter(complaint=self.request.query_params["complaint_id"])
        # .values('id', 'created', 'email', 'email_count', 'status', 'status_value')

        # print(f'qs = {qs}')

        return qs


@permission_classes([IsAuthenticated])
class ComplaintSetStatus(generics.GenericAPIView):
    """
    Set Order Status
    """
    # parser_classes = (MultiPartParser, FormParser)
    # queryset = models.Uplist.objects.all()
    # serializer_class = serializers.UplistSerializer
    serializer_class = ComplaintSetStatusSerializer

    # serializers = OrderSetStatusSerializer

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Complaint, id=request.data['id'],
                                  status__in=[STATUS.waiting, STATUS.processing])
        # order = Order.get_ob objects.filter(id=request.data['id'], status__in=[0, 1]).update(status=3)
        order.status = STATUS.cancelled
        order.save()

        # added function here
        return Response()


@permission_classes([IsAuthenticated])
class ProductView(ModelViewSet):
    """
    Get user product
    """

    serializer_class = ProductSerializer

    def get_queryset(self, ):
        qs = Product.objects.filter(user=self.request.user)
        # .values('id', 'created', 'email', 'email_count', 'status', 'status_value')

        return qs


@permission_classes([IsAuthenticated])
class ProductDelete(generics.GenericAPIView):
    """
    Delete Product (not yet accepted)
    """

    # parser_classes = (MultiPartParser, FormParser)
    # queryset = models.Uplist.objects.all()
    # serializer_class = serializers.UplistSerializer
    serializer_class = ComplaintSetStatusSerializer

    # serializers = OrderSetStatusSerializer

    def post(self, request, *args, **kwargs):
        qs = Product.objects.filter(id=int(self.request.data['id']), user=self.request.user,
                                    status__in=[PRODUCT_STATUS.waiting])
        qs.delete()

        return Response()


# region 'internal services'
class APIKeyAuthentication(TokenAuthentication):
    """
    API Key token based authentication
    """

    def authenticate(self, request):
        user = None
        token = request.data.get('api_key', None)

        if API_KEY_INTERNAL != token:
            raise exceptions.AuthenticationFailed('Invalid API Key.')

        return user, token


# class GetSitesList(generics.ListAPIView):
#     """
#     Get sites list from url/search text
#     """
#     serializer_class = GetSitesListSerializer
#     authentication_classes = (APIKeyAuthentication,)
#
#     # def get_serializer(self, *args, **kwargs):
#     #     serializer_class = self.get_serializer_class()
#     #     kwargs['context'] = self.get_serializer_context()
#     #     # if self.action == 'create':
#     #     #     kwargs['many'] = True
#     #     return serializer_class(*args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         search_text = self.request.data['search_text']
#         product_name = self.request.data['product_name']
#         results_count = int(self.request.data['results_count'])
#
#         res = get_sites_list(search_text, product_name, results_count)
#         return Response(res)
#
#
# class GetSiteHosting(generics.GenericAPIView):
#     """
#     Get site hosting (for internal use only)
#     """
#     serializer_class = SiteHostingSerializer
#     authentication_classes = (APIKeyAuthentication,)
#
#     def post(self, request, *args, **kwargs):
#         url = self.request.data['url']
#
#         res = get_site_hosting(url)
#         return HttpResponse(res)
#
#
# class GetSiteHostingAbuseEmail(generics.GenericAPIView):
#     """
#     Get site hosting abuse email (for internal use only)
#     """
#     serializer_class = SiteHostingAbuseEmailSerializer
#     authentication_classes = (APIKeyAuthentication,)
#
#     def post(self, request, *args, **kwargs):
#         res = None
#         url = self.request.data['url']
#
#         res = get_site_hosting_abuse_email(url)
#         return HttpResponse(res)
#
#
# class GetSiteScreenshot(generics.GenericAPIView):
#     """
#     Get site screenshot (for internal use only)
#     """
#     serializer_class = SiteScreenshotSerializer
#     authentication_classes = (APIKeyAuthentication,)
#
#     def post(self, request, *args, **kwargs):
#         url = self.request.data['url']
#
#         res = get_site_screenshot(url)
#         return HttpResponse(res, content_type="image/png")
#

class AnonymousSearch(APIView):
    """
    Simple mathematical convert function for anonymous search
    """

    def post(self, request, *args, **kwargs):
        s = request.data['search_text']
        # i = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10 ** 8

        i = randrange(99, 500)
        return Response({
            'search_results': i
        })

# endregion
