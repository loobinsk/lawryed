# from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import send_mail
from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from django.template.loader import render_to_string
from django.urls import reverse
# from django.utils.html import strip_tags
# from django.views import View
from django.views.generic import CreateView

from products.forms import ProductForm
from products.models import Product, PRODUCT_STATUS
from lawyerd.users.models import Company


class ProductCreateView(LoginRequiredMixin, CreateView):
    # model = Product
    template_name = 'pages/products.html'
    form_class = ProductForm

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = self.request.user
        model.document_file_name = self.request.FILES['document'].name
        if self.request.user.is_superuser:
            model.status = PRODUCT_STATUS.accepted

        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('products')


product_create_view = ProductCreateView.as_view()
