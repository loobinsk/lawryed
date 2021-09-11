from allauth.account.views import password_change
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns
from rest_framework_swagger.views import get_swagger_view

# from company.views import company_update_view
from products.views import product_create_view
from project.views import home_view, oops_view
from lawyerd.users.views import company_update_view

schema_view = get_swagger_view(title='Lawyerd API')

urlpatterns = [
        # path('capture/',  include('screamshot.urls', namespace='screamshot'), name='screamshot'),
        path('api/', schema_view, name='swagger'),
<<<<<<< HEAD
        path("", view=home_view, name="home"),
        path('api/v1/', include('api.v1.urls')),
        path("users/", include("users.urls", namespace="users")),
        path("accounts/", include("allauth.urls")),
=======
        path('api/v1/', include('api.v1.urls')),
        path("oops/", view=oops_view, name="oops"),
        # path('feedback/', view=company_update_view),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
        path('rosetta/', include('rosetta.urls')),
        # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
        path("", view=home_view, name="home"),
        path("faq/", TemplateView.as_view(template_name="pages/faq.html"), name="faq"),
        path("about_us/", TemplateView.as_view(template_name="pages/about_us.html"), name="about_us"),
        path("contact_us/", TemplateView.as_view(template_name="pages/contact_us.html"), name="contact_us"),



        path("terms/", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),
        path("policy/", TemplateView.as_view(template_name="pages/policy.html"), name="policy"),

        # path("profile/", TemplateView.as_view(template_name="account/password_change.html"), name="profile"),
>>>>>>> c8fa8806f6ba7e69e0a9ad2a011318c9a57a10ab
        path("profile/", password_change, {'template_name': 'account/password_change.html', }, name="profile"),

        path("company/", view=company_update_view, name="company"),
        path("products/", view=product_create_view, name="products"),
        # path("pricing_old/", TemplateView.as_view(template_name="pages/pricing.html"), name="pricing_old"),

        # Django Admin, use {% url 'admin:index' %}
        path(settings.ADMIN_URL, admin.site.urls),

        # Your stuff: custom urls includes go here
        path('explorer/', include('explorer.urls')),

        path('products/', include('products.urls')),
        path('orders/', include('complaint.urls')),
        path('feedback/', include('feedback.urls')),
        path('plans-payments/', include('plans_payments.urls')),
        path('plan/', include('plans.urls')),
        # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"), 
        # path('feedback/', view=company_update_view),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
        path('rosetta/', include('rosetta.urls')),
        # path("profile/", TemplateView.as_view(template_name="account/password_change.html"), name="profile"),
        path("terms/", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),  
        path("policy/", TemplateView.as_view(template_name="pages/policy.html"), name="policy"),
        # User management
        path("faq/", TemplateView.as_view(template_name="pages/faq.html"), name="faq"),  
        path("about_us/", TemplateView.as_view(template_name="pages/about_us.html"), name="about_us"),  
        path("contact_us/", TemplateView.as_view(template_name="pages/contact_us.html"), name="contact_us"),
        path("oops/", view=oops_view, name="oops"),
    )

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
