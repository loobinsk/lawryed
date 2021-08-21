from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models.functions import Now
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

# from complaint.tasks import compliant_work
# from complaint.models import send_complaint_email, test_send_complaint_email
from lawyerd.users.models import Company
from users.forms import CompanyForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name", ]

    # fields = ["name", "company_name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class CompanyCreateUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    success_message = "Company info updated successfully"
    template_name = 'pages/company.html'

    def get_success_url(self):
        return reverse('company', kwargs={})

    def get_object(self, queryset=None):
        obj = Company.objects.filter(user=self.request.user).first()
        if not obj:
            obj, created = Company.objects.get_or_create(user=self.request.user, owner_date=Now())

        obj, created = Company.objects.get_or_create(user=self.request.user)
        return obj


company_update_view = CompanyCreateUpdateView.as_view()
