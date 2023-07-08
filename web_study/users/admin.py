from django.contrib import admin

from models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'password'
    )


admin.site.register(User, UserAdmin)
