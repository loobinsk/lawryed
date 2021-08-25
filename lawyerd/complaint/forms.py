from django import forms
from django.utils.translation import gettext_lazy as _
from complaint.models import Order


class CreateOrderForm(forms.ModelForm):
    email = forms.EmailField(label=_('Enter e-mail'))
    email_count = forms.IntegerField(label=_('Enter e-mail count'), min_value=1)

    class Meta:
        model = Order
        fields = ('email', 'email_count',)
