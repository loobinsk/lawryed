from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PosterConfig(AppConfig):
    name = "lawyerd.poster"
    verbose_name = _("Poster")

    def ready(self):
        # import poster.signals  # noqa F401

        import poster.signals  # noqa F401

        # try:
        #     print('try import')
        #     import poster.signals  # noqa F401
        #     print('imported')
        # except Exception as e:
        #     print(f'Import error: {e}')
