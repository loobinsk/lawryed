from django import forms

from complaint.models import Order


class CreateOrderForm(forms.ModelForm):
    email = forms.EmailField(label='Enter e-mail')
    email_count = forms.IntegerField(label='Enter e-mail count', min_value=1)

    class Meta:
        model = Order
        fields = ('email', 'email_count',)
