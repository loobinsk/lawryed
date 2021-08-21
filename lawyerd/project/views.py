from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from lawyerd.users.models import Company
from products.models import Product, PRODUCT_STATUS


def validate_oops_page(request):
    filled_company = Company.objects.filter(user=request.user, owner_name__isnull=False).exists()
    filled_products = Product.objects.filter(user=request.user).exists()
    filled_userplan = request.user.is_superuser or not request.user.userplan.plan.default

    res = {
        'filled_company': filled_company,
        'filled_products': filled_products,
        'filled_payments_plan': filled_userplan,
        'show_oops_page': not (filled_company and filled_userplan and filled_userplan)
    }

    return res


class OoopsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/oops.html', {'context': validate_oops_page(self.request)})


oops_view = OoopsView.as_view()


class HomeView(View):
    def get(self, request, *args, **kwargs):


        # import complaint.models as data_module
        # Company = data_module.Company
        # Product = data_module.Product
        #
        # Complaint = data_module.Complaint
        # ComplaintDetail = data_module.ComplaintDetail
        #
        #
        # def getModelFields(modelName):
        #     x = [f"'{modelName._meta.model_name}.{x.attname}'".replace("'", '') for x in modelName._meta.get_fields()
        #          if hasattr(x, 'attname')]
        #     return x
        #
        # all_fields = getModelFields(Product) + getModelFields(Company) + getModelFields(Complaint) + \
        #              getModelFields(ComplaintDetail)

        # res = {}
        if self.request.user.is_authenticated:
            products = Product.objects.filter(user=self.request.user, status__in=[PRODUCT_STATUS.accepted, ]).values(
                'id', 'name')
            res = {'products': products}
            # res = {'products': products, 'app_label': 'auth', 'model_name': 'user'}

            return render(request, "pages/home_authorized.html", {'context': res})
        else:
            return render(request, "pages/home_unauthorized.html")


home_view = HomeView.as_view()
