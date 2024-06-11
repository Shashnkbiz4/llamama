# superadmin/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SuperAdmin, Client

class SuperAdminAdmin(UserAdmin):
    model = SuperAdmin
    list_display = ('email', 'is_superadmin', 'is_clientadmin', 'is_staff', 'is_active')
    list_filter = ('is_superadmin', 'is_clientadmin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superadmin', 'is_clientadmin', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_superadmin', 'is_clientadmin', 'is_staff', 'is_active', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(SuperAdmin, SuperAdminAdmin)


admin.site.register(Client)
