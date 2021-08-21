from abc import ABC

from rest_framework import serializers
from complaint.models import Complaint, ComplaintDetail, STATUS

from django.db.models.expressions import Case, When
# from django.db.models.functions import RowNumber
# from django.db.models import F
# from django.db.models import Value, Sum, IntegerField, Window, Count
from django.db.models import Count

# from lawyerd.users.models import Assets  # !!!!!!!!!!!!
from products.models import Product


class ComplaintSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # created = serializers.DateTimeField()
    # referral_string = serializers.CharField()

    product = serializers.ReadOnlyField(source='product__name', read_only=True)

    class Meta:
        model = Complaint
        fields = (
            'id',
            'created',
            'modified',
            'product',
            'search_text',
            # 'email',
            # 'site_count',
            'status',
            'status_value',
        )

    # def __init__(self, *args, **kwargs):
    #     super(SiteOrdersSerializer, self).__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        context = kwargs.pop("context")

        # TODO: swagger hack
        # https://stackoverflow.com/questions/17906936/indexerror-tuple-index-out-of-range
        # if not args:
        #     return None
        #     super(ComplaintSerializer, self).__init__(*args, **kwargs)

        qs_site_orders = args[0]
        # append extra data

        # if len(qs_orders) == 0:
        #     return qs_orders

        qs_queue = Complaint.get_active().values('id', 'row_number')

        qs_processing = ComplaintDetail.objects.filter(complaint__user=context['request'].user,
                                                       complaint__status=STATUS.processing)
        qs_processing = qs_processing.values('complaint_id').annotate(
            count=Count('id'),
            ok=Count(Case(When(status=STATUS.ok, then=1))),
            error=Count(Case(When(status=STATUS.error, then=1))),
        )

        for item in qs_site_orders:
            # status_value = item['status_value']
            # status = item.status
            status = item['status']

            # get queue position
            if status == STATUS.waiting:
                for queue_item in qs_queue:
                    # if queue_item['id'] == item['id']:
                    if queue_item['id'] == item['id']:
                        item['status_value'] = queue_item['row_number']
                        # break

            # get progress procent
            elif status == STATUS.processing:
                for processing_item in qs_processing:
                    if processing_item['complaint_id'] == item['id']:
                        item['status_value'] = round(
                            ((processing_item['ok'] + processing_item['error']) / processing_item['count']) * 100)
                        # break

            # complete, just pass
            elif status == STATUS.ok:
                pass

        # self.college_id = context.get('college_id')
        super(ComplaintSerializer, self).__init__(*args, **kwargs)


class ComplaintSetStatusSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        pass

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def to_internal_value(self, data):
        pass


class ComplaintDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintDetail
        # fields = '__all__'
        fields = (
            'id',
            # 'order_id',
            'created',
            #################
            'site',
            # 'hosting',
            # 'email',
            'screenshot',
            'status',
        )


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # created = serializers.DateTimeField()
    # referral_string = serializers.CharField()

    class Meta:
        model = Product
        # fields = '__all__'
        fields = (
            'id',
            'created',
            'itype',
            'name',
            'document',
            'document_file_name',
            'status',
        )


class SiteHostingSerializer(serializers.BaseSerializer):
    pass


class SiteHostingAbuseEmailSerializer(serializers.BaseSerializer):
    pass


class SiteScreenshotSerializer(serializers.BaseSerializer):
    pass


class GetSitesListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        pass

    def create(self, validated_data):
        pass

    def to_internal_value(self, data):
        pass
