from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from users.forms import UserChangeForm, UserCreationForm
from lawyerd.users.models import Company

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("redirected_email", "name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "redirected_email", "is_superuser"]
    search_fields = ['id', "name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    # list_filter = ('status',)
    list_display = ["id", "user", "title"]
    search_fields = ['id', "email", 'user', 'title']
