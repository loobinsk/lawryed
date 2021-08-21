import posixpath

from django import forms
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext, ugettext_lazy as _

from dbtemplates.conf import settings
from dbtemplates.models import (Template, remove_cached_template,
                                add_template_to_cache)
from dbtemplates.utils.template import check_template_syntax
# Check if django-reversion is installed and use reversions' VersionAdmin
# as the base admin class if yes
from products.models import Product

if settings.DBTEMPLATES_USE_REVERSION:
    from reversion.admin import VersionAdmin as TemplateModelAdmin
else:
    from django.contrib.admin import ModelAdmin as TemplateModelAdmin  # noqa


class CodeMirrorTextArea(forms.Textarea):
    """
    A custom widget for the CodeMirror browser editor to be used with the
    content field of the Template model.
    """

    class Media:
        css = dict(screen=[posixpath.join(
            settings.DBTEMPLATES_MEDIA_PREFIX, 'css/editor.css')])
        js = [posixpath.join(settings.DBTEMPLATES_MEDIA_PREFIX, 'js/codemirror.js')]

        ################################
        css = dict(screen=[posixpath.join(
            # settings.DBTEMPLATES_MEDIA_PREFIX,
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/codemirror.min.css'),

            posixpath.join(
                # settings.DBTEMPLATES_MEDIA_PREFIX,
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/hint/show-hint.min.css'),

            posixpath.join(
                # settings.DBTEMPLATES_MEDIA_PREFIX,
                '%(media_prefix)scss/django.css') % dict(media_prefix=settings.DBTEMPLATES_MEDIA_PREFIX),


        ])


        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/codemirror.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/mode/overlay.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/hint/show-hint.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/mode/django/django.min.js',


            # '%(media_prefix)sjs/parsedjango.js' % dict(media_prefix=settings.DBTEMPLATES_MEDIA_PREFIX),
        ]


        # <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/hint/show-hint.min.css" integrity="sha512-OmcLQEy8iGiD7PSm85s06dnR7G7C9C0VqahIPAj/KHk5RpOCmnC6R2ob1oK4/uwYhWa9BF1GC6tzxsC8TIx7Jg==" crossorigin="anonymous" />
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/hint/show-hint.min.js" integrity="sha512-0DOTP7HSS4G4YFu9YSLmHMmzSUQmK136iJLWMmy3TxaDBI6K/r9NSo7+5LmwPjwW97EkR5VT8qdRoLqv/D/TeQ==" crossorigin="anonymous"></script>
        #
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/hint/javascript-hint.min.js" integrity="sha512-2zi+0HSB5MXoy+BenDX/EKjqN6eUnsG2Lh9cpx+Ckua3Yi2XupO8ife9VELSg8iR7AT98yHQNyyaAL4ImVHcoQ==" crossorigin="anonymous"></script>
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/mode/markdown/markdown.min.js" integrity="sha512-0K+rqJScVAdCA5qtj1uJ4QR9BVJdqwr5rWidqGKQ/7brmV0ICc2ginZVvjwCPPvIns7Ea8xCkr/X/7rgxe7biw==" crossorigin="anonymous"></script>
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/mode/sql/sql.min.js" integrity="sha512-dfObApt1XdGl62IJLrjbIOc9QtnRORA5TCwdnJkSj6C/KjwMz2L/Sc4WlcrgAuWoY+n5xTf6NMMojoUOlgwjug==" crossorigin="anonymous"></script>
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/hint/javascript-hint.min.js" integrity="sha512-2zi+0HSB5MXoy+BenDX/EKjqN6eUnsG2Lh9cpx+Ckua3Yi2XupO8ife9VELSg8iR7AT98yHQNyyaAL4ImVHcoQ==" crossorigin="anonymous"></script>
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/addon/hint/html-hint.min.js" integrity="sha512-oxBKDzXElkyh3mQC/bKA/se1Stg1Q6fm7jz7PPY2kL01jRHQ64IwjpZVsuZojcaj5g8eKSMY9UJamtB1QR7Dmw==" crossorigin="anonymous"></script>


    @staticmethod
    def getModelFields(modelName):
        x = [f"'{modelName._meta.model_name}.{x.attname}'" for x in modelName._meta.get_fields() if
             hasattr(x, 'attname')]
        return x

    def render(self, name, value, attrs=None, renderer=None):
        # from users.models import Company

        s = """
        company.id
        company.created
        company.modified
        company.user_id
        company.company_name
        company.owner_name
        company.owner_surname
        company.title
        company.address_country
        company.address_city
        company.address_street
        company.address_state
        company.address_zip
        company.region
        company.owner_date
        company.products
        company.email
        company.additional
        company.additional2
        company.confirmation
        company.website
        company.terms
        company.phone
        company.youtube
        company.document
        company.document_right
        """


        # pass
        #
        #
        all_fields = []
        all_fields = CodeMirrorTextArea.getModelFields(Product)
        # all_fields = CodeMirrorTextArea.getModelFields(Company)
        all_fields_str = ', '.join(all_fields).replace('\\', '')

        all_fields_str = all_fields_str + ''

        result = []  # noqa
        result.append(
            super(CodeMirrorTextArea, self).render(name, value, attrs))

        #   var editor = CodeMirror.fromTextArea('id_%(name)s', {

        # parserfile: "parsedjango.js",
        # stylesheet: "%(media_prefix)scss/django.css",
        #     mode: "text/x-django",
        # parserfile: "parsedjango.js"
        # mode: "django",

        result.append(u"""
<script type="text/javascript">
  let productList2 = [    'Electronics Watch',    'House wear Items',    'Kids wear',    'Women Fashion'];
  let productList = ['product.id', 'product.created', 'product.modified', 'product.user_id', 'product.name', 'product.document', 'product.document_file_name', 'product.status', 'product.itype', 'company.id', 'company.created', 'company.modified', 'company.user_id', 'company.company_name', 'company.owner_name', 'company.owner_surname', 'company.title', 'company.address_country', 'company.address_city', 'company.address_street', 'company.address_state', 'company.address_zip', 'company.region', 'company.owner_date', 'company.products', 'company.email', 'company.additional', 'company.additional2', 'company.confirmation', 'company.website', 'company.terms', 'company.phone', 'company.youtube', 'company.document', 'company.document_right', 'complaint.id', 'complaint.created', 'complaint.modified', 'complaint.user_id', 'complaint.product_id', 'complaint.search_text', 'complaint.email', 'complaint.site_count', 'complaint.status', 'complaint.finished', 'complaintdetail.id', 'complaintdetail.created', 'complaintdetail.modified', 'complaintdetail.complaint_id', 'complaintdetail.site', 'complaintdetail.hosting', 'complaintdetail.email', 'complaintdetail.screenshot', 'complaintdetail.status'];


  var editor = CodeMirror.fromTextArea(document.getElementById('id_%(name)s'), {

    path: "%(media_prefix)sjs/",



    continuousScanning: 500,
    tabMode: "shift",
    indentUnit: 4,
    lineNumbers: true,

    showHint: true,

    mode: "text/x-django",

  });


</script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="/staticfiles/js/params.js"></script>


""" % dict(media_prefix=settings.DBTEMPLATES_MEDIA_PREFIX, name=name, all_fields_str=all_fields_str))
        return mark_safe(u"".join(result))


if settings.DBTEMPLATES_USE_CODEMIRROR:
    TemplateContentTextArea = CodeMirrorTextArea
else:
    TemplateContentTextArea = forms.Textarea

if settings.DBTEMPLATES_AUTO_POPULATE_CONTENT:
    content_help_text = _("Leaving this empty causes Django to look for a "
                          "template with the given name and populate this "
                          "field with its content.")
else:
    content_help_text = ""

if settings.DBTEMPLATES_USE_CODEMIRROR and settings.DBTEMPLATES_USE_TINYMCE:
    raise ImproperlyConfigured("You may use either CodeMirror or TinyMCE "
                               "with dbtemplates, not both. Please disable "
                               "one of them.")

if settings.DBTEMPLATES_USE_TINYMCE:
    from tinymce.widgets import AdminTinyMCE  # noqa

    TemplateContentTextArea = AdminTinyMCE
elif settings.DBTEMPLATES_USE_REDACTOR:
    from redactor.widgets import RedactorEditor  # noqa

    TemplateContentTextArea = RedactorEditor


class TemplateAdminForm(forms.ModelForm):
    """
    Custom AdminForm to make the content textarea wider.
    """
    content = forms.CharField(
        widget=TemplateContentTextArea(attrs={'rows': '24'}),
        help_text=content_help_text, required=False)

    class Meta:
        model = Template
        fields = ('name', 'content', 'sites', 'creation_date', 'last_changed')
        fields = "__all__"


class TemplateAdmin(TemplateModelAdmin):
    form = TemplateAdminForm
    fieldsets = (
        (None, {
            'fields': ('name', 'content'),
            'classes': ('monospace',),
        }),
        (_('Advanced'), {
            'fields': (('sites'),),
        }),
        (_('Date/time'), {
            'fields': (('creation_date', 'last_changed'),),
            'classes': ('collapse',),
        }),
    )
    filter_horizontal = ('sites',)
    list_display = ('name', 'creation_date', 'last_changed', 'site_list')
    list_filter = ('sites',)
    save_as = True
    search_fields = ('name', 'content')
    actions = ['invalidate_cache', 'repopulate_cache', 'check_syntax']

    def invalidate_cache(self, request, queryset):
        for template in queryset:
            remove_cached_template(template)
        count = queryset.count()
        message = ungettext(
            "Cache of one template successfully invalidated.",
            "Cache of %(count)d templates successfully invalidated.",
            count)
        self.message_user(request, message % {'count': count})

    invalidate_cache.short_description = _("Invalidate cache of "
                                           "selected templates")

    def repopulate_cache(self, request, queryset):
        for template in queryset:
            add_template_to_cache(template)
        count = queryset.count()
        message = ungettext(
            "Cache successfully repopulated with one template.",
            "Cache successfully repopulated with %(count)d templates.",
            count)
        self.message_user(request, message % {'count': count})

    repopulate_cache.short_description = _("Repopulate cache with "
                                           "selected templates")

    def check_syntax(self, request, queryset):
        errors = []
        for template in queryset:
            valid, error = check_template_syntax(template)
            if not valid:
                errors.append('%s: %s' % (template.name, error))
        if errors:
            count = len(errors)
            message = ungettext(
                "Template syntax check FAILED for %(names)s.",
                "Template syntax check FAILED for %(count)d templates: %(names)s.",
                count)
            self.message_user(request, message %
                                       {'count': count, 'names': ', '.join(errors)})
        else:
            count = queryset.count()
            message = ungettext(
                "Template syntax OK.",
                "Template syntax OK for %(count)d templates.", count)
            self.message_user(request, message % {'count': count})

    check_syntax.short_description = _("Check template syntax")

    def site_list(self, template):
        return ", ".join([site.name for site in template.sites.all()])

    site_list.short_description = _('sites')


admin.site.register(Template, TemplateAdmin)
