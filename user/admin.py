from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from user.forms import UserChangeForm, UserCreationForm
from user.models import Dev,Hr,Bio, Project, Skill,Vouch

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("User", {"fields":("name",)}),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username","name","is_superuser","type"]
    search_fields = ["name"]

admin.site.register(Dev)
admin.site.register(Hr)
admin.site.register(Bio)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Vouch)