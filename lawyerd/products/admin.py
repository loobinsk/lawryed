from django.contrib import admin

# from domains.models import Domain

from django.db import connection
from django.core.paginator import Paginator

from products.models import Product


# admin.site.register(Product)


# ################# Admin Utils
class LargeTablePaginator(Paginator):
    """
    Warning: Postgresql only hack
    Overrides the count method of QuerySet objects to get an estimate instead of actual count when not filtered.
    However, this estimate can be stale and hence not fit for situations where the count of objects actually matter.
    """

    def _get_count(self):
        if getattr(self, '_count', None) is not None:
            return self._count

        query = self.object_list.query
        if not query.where:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s",
                               [query.model._meta.db_table])
                self._count = int(cursor.fetchone()[0])
            except:
                self._count = super(LargeTablePaginator, self)._get_count()
        else:
            self._count = super(LargeTablePaginator, self)._get_count()

        return self._count

    count = property(_get_count)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'site', 'checked', 'alive', 'forms',)
#
#     search_fields = ('site',)
#
#
#     show_full_result_count = False
#     paginator = LargeTablePaginator


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_filter = ('status', 'itype')
    list_display = ["id", "user", "document", "status", 'itype']
    search_fields = ['id', "document"]
