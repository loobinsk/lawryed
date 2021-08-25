from fileinput import FileInput

# from bootstrap_datepicker_plus import DatePickerInput
from captcha import widgets
from crispy_forms.bootstrap import StrictButton, FormActions
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Input
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm, Textarea, URLInput, FileField, FileInput, CharField, TextInput, DateInput, ClearableFileInput, Form
from allauth.account.forms import SignupForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row, Column, Field

from products.models import Product

User = get_user_model()

CustomClerableFileField = FileInput(
    attrs={  # 'type': 'file',
        'accept': 'application/pdf',
        # 'class': "file",
        # 'data-show-preview': "false"
    })


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["itype", "name", "document"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # self.fields['owner_date'].widget = DateInput(attrs={'type': 'date', 'required': ''})

        self.helper = FormHelper()
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('products')

        self.helper.layout = Layout(

            Row(
                Column('itype', css_class='col-md-2'),
                Column('name'),
                Column(Field('document', accept='application/pdf')),
            ),

            Submit('submit', _('Add product'))
        )
