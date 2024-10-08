from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User # 確保這裡正確導入了你的 User 模型
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

class UserAdmin(BaseUserAdmin):
    # exclude = ('email',) 本來有這個 
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'avatar')
    readonly_fields = ('date_joined', )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('個人資訊', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('權限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要的日子', {'fields': ('last_login', 'date_joined')}), 
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'avatar'),
        }),
    )
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     ('Profile', {'fields': ('avatar',)}),
    # )

admin.site.register(User, UserAdmin)