from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User # 確保這裡正確導入了你的 User 模型
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    # exclude = ('email',) 本來有這個 
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    readonly_fields = ('date_joined', )  # 注意這裡是一個元組

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}), 
    )

admin.site.register(User, UserAdmin)