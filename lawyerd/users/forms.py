from fileinput import FileInput

# from bootstrap_datepicker_plus import DatePickerInput
from captcha import widgets
from crispy_forms.bootstrap import StrictButton, FormActions
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Input
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm, Textarea, URLInput, FileField, FileInput, CharField, TextInput, DateInput, \
    ClearableFileInput
from allauth.account.forms import SignupForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row, Column, Field, MultiField

from captcha.fields import ReCaptchaField

from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget

from lawyerd.users.models import Company
from django_countries.widgets import CountrySelectWidget

User = get_user_model()

# <input id="input-b2" name="input-b2" type="file" class="file" data-show-preview="false">
# <input type="file" name="document" accept="application/pdf" data-show-preview="false" class="fileinput fileUpload" required id="id_document">


# <input type="file" name="document" value="9623ca.pdf" accept="application/pdf" class="file input form-control" data-show-preview="false" required id="id_document">

CustomClerableFileField = FileInput(
    attrs={  # 'type': 'file',
        'accept': 'application/pdf',
        # 'class': "file",
        # 'data-show-preview': "false"
    })


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class CustomSignupForm(SignupForm):
    # company_name = CharField(max_length=255, label=_('Company name'), required=True)
    # company_name = CharField(max_length=255, label=_('Company name'), required=True)

    # https://developers.google.com/recaptcha/docs/display#js_param
    captcha = ReCaptchaField(
        widget=widgets.ReCaptchaV2Checkbox(
            api_params={'hl': 'en', 'onload': 'onLoadFunc'}
        )
    )

    # last_name = CharField(max_length=30, label='Last Name')

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = _('Email')
        # self.fields['company_name'].widget.attrs['placeholder'] = _('Company name')

        self.fields['password2'].label = _('Confirm password')
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label

        self.fields['username'].label = _('Username')
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label

        # self.fields['company_name'].widget.attrs['placeholder'] = _('Company name')

        # self.fields["captcha"] = ReCaptchaField()
        self.fields['captcha'].label = False

        self.helper = FormHelper()

        collumn_css_class = 'form-group col-md-6 mb-0'
        form_css_class = 'form-row'

        self.helper.layout = Layout(
            Fieldset(
                None,  # legend
                Row(
                    Column('email', css_class=collumn_css_class),
                    # Column('username', css_class=collumn_css_class),
                    css_class=form_css_class
                ),

                Row(
                    # Column('email', css_class=collumn_css_class),
                    Column('username', css_class=collumn_css_class),
                    css_class=form_css_class
                ),

                Row(
                    Column('password1', css_class=collumn_css_class),
                    # Column('company_name', css_class=collumn_css_class),
                    css_class=form_css_class
                ),
                Row(
                    Column('password2', css_class=collumn_css_class),
                    css_class=form_css_class
                ),

                Row(
                    Column('captcha', css_class=collumn_css_class),
                    css_class=form_css_class
                ),
            ),
            ButtonHolder(
                Submit('submit', _('Registration'))
                # Submit('submit', _('Registration'), css_class='button white')
            )
        )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user

    def signup(self, request, user):
        # user.company_name = self.cleaned_data['company_name']
        user.save()
        return user


FormClearableFileInput = ClearableFileInput()


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        # fields = '__all__'
        exclude = ['user']
        widgets = {'country': CountrySelectWidget()}
        # fields = '__all__'

        # fields = [
        #     'company_name',
        #     'owner_name',
        #     'owner_surname',
        #     'title',
        #     'address',
        #     'region',
        #     'owner_date',
        #     'products',
        #     'document_right',
        #     'document',
        #
        #     'email',
        #     'additional',
        #     'additional2',
        #     'confirmation',
        #     'website',
        #     'phone',
        #     'youtube',
        # ]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.fields['owner_date'].widget = DateInput(attrs={'type': 'date', 'required': ''})
        # self.fields['address_country'].widget = DateInput(attrs={'type': 'date', 'required': ''})

        self.fields['address_country'].widget.attrs['style'] = 'height: 23px; padding: 0px'

        # self.fields['document'].widget = CustomClerableFileField
        # self.fields['document_right'].widget = CustomClerableFileField
        # self.fields['phone'].widget = PhoneNumberPrefixWidget()
        # self.fields['phone'].widget = PhoneNumberPrefixWidget(attrs={'class': "form-control"})

        # self.fields['password2'].label = _('Confirm password')
        # self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label
        # self.fields['username'].label = _('Full name')
        # self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label
        # self.fields['captcha'].label = False

        # self.fields['password'].widget = forms.PasswordInput()
        # self.helper = FormHelper(self)
        # self.helper.col_class = False
        # self.helper.form_tag = False
        # self.helper.form_show_labels = True
        #
        # for field in self.fields:
        #     self.fields[field].widget.attrs['placeholder'] = None
        #     del self.fields[field].widget.attrs['placeholder']
        #
        # self.helper.layout = Layout(
        #     'login', 'password', 'remember',
        #     StrictButton(
        #         'Sign In', type='submit', style='margin-top: 10px',
        #         css_class="waves-effect btn-large blue waves-light btn right"),
        # )

        self.helper = FormHelper()
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('company')

        self.helper.layout = Layout(
            Row(
                Column('company_name'),
                Column('email'),
            ),

            Row(
                Column('owner_name'),
                Column('additional'),
            ),

            Row(
                Column('owner_surname'),
                Column('additional2'),
            ),

            Row(
                Column('title'),
                Column('confirmation'),
            ),

            Row(
                Column(
                    Field('address_country', wrapper_class='col-md-3'),
                    Field('address_city', wrapper_class='col-md-3'),
                    Field('address_street', wrapper_class='col-md-3'),
                    Field('address_state', wrapper_class='col-md-3'),
                    # Field('address_zip', wrapper_class='col-md-3'),
                    css_class='form-row form-row_country'
                ),
            ),

            Row(
                Column('website'),
            ),

            Row(
                Column('address_zip'),
                Column('terms'),
            ),

            Row(
                Column('region'),
                Column('phone'),
            ),

            Row(
                Column('owner_date'),
                Column('youtube'),
            ),

            Row(
                Column('products'),
                # Column('products'),
            ),

            Row(
                # , css_class='file'
                Column(Field('document', accept='application/pdf')),
                Column(Field('document_right', accept='application/pdf')),
                # Column('document_right'),
            ),

            Submit('submit', _('Update'))

            # ButtonHolder(
            #     Submit('submit', _('Update'), css_class="btn btn-primary")
            #     # Submit('submit', _('Registration'), css_class='button white')
            # )
        )

    def save(self, commit=True):
        instance = super(CompanyForm, self).save(commit=False)
        # instance.course = self.course
        # instance.user = self.user
        if commit:
            instance.save()
        return instance

        # ###########################

        # phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
        # def form_valid(self, form):
        #     form.instance.created_by = self.request.user
        #     return super().form_valid(form)
        #
        # def __init__(self, *args, **kwargs):
        #     # create an HTML5 placeholder attribute based on the field help_text
        #     for field_name in self.fields:
        #         field = self.fields.get(field_name)
        #         if field:
        #             if type(field.widget) == TextInput:
        #                 field.widget.attrs["placeholder"] = field.help_text
        #

        # class Meta:
        #     model = Company
        #     fields = '__all__'
        #     # exclude = ['user']
        #
        #     # labels = {
        #     #     'additional': 'dfdfgdfg'
        #     # }
        #
        #     widgets = {
        #         # 'title': Textarea(attrs={'cols': 80, 'rows': 20}),
        #         # 'title': Textarea(),
        #         'phone': PhoneNumberPrefixWidget(),
        #         # 'youtube': URLInput(),
        #         # 'owner_date': DateInput(attrs={'required': ''}),
        #         # 'owner_date': DatePickerInput(format='%Y-%m-%d'),
        #         # 'document': FileInput(attrs={'accept': 'application/pdf'})
        #         # 'document': ClearableFileInput(attrs={'accept': 'application/pdf'}),
        #         'document': ClearableFileInput(),
        #         'document_right': ClearableFileInput(),
        #     }
        #
