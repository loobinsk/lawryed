from django.contrib import admin
# from domains.models import Domain
from django.db.models import QuerySet
import logging

from django.utils.safestring import mark_safe

from complaint.models import Complaint, ComplaintDetail


# admin.site.register(Complaint)
# admin.site.register(ComplaintDetail)
# dfgdfg

@admin.register(ComplaintDetail)
class ComplaintDetailAdmin(admin.ModelAdmin):
    # class ComplaintDetailAdmin(admin.TabularInline):
    # model = ComplaintDetail
    # form = UserChangeForm
    # add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_filter = ('status',)
    list_display = ["id", 'created', 'site', 'hosting', 'email', 'template_name', 'image_tag', "status"]
    search_fields = ['id', 'site', 'hosting', ]

    def image_tag(self, item):
        res = '-'

        if item.screenshot and hasattr(item.screenshot, 'url'):
            res = mark_safe(f'<img src="{item.screenshot.url}" width="100" height="100" />')  # Get Image url
        return res

    image_tag.short_description = 'screenshot'


class ComplaintDetailInlineAdmin(admin.TabularInline):
    model = ComplaintDetail
    # form = UserChangeForm
    # add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    # list_filter = ('status',)
    # exclude = ['id',]
    list_filter = ('status',)
    readonly_fields = ['id', 'created', ]
    fields = ('id', 'created', 'site', 'hosting', 'email', 'screenshot', 'status')
    # show_change_link = True

    # fields = ["id", ]
    # search_fields = ['id', 'site', 'hosting', ]

    # def image_tag(self, item):
    #     return mark_safe('<img src="%s" width="100" height="100" />' % (
    #         item.screenshot.url))  # Get Image url
    #
    # image_tag.short_description = 'screenshot'
    extra = 1


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_filter = ('status',)
    list_display = ["id", 'created', "user", 'search_text', "status"]
    search_fields = ['id', 'search_text']
    inlines = [ComplaintDetailInlineAdmin]
