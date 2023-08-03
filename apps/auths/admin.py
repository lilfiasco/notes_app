from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """CustomUserAdmin."""

    list_display = ('email',)
    list_filter = ('email', 'nickname',)
    search_fields = ('email', 'nickname',)
    filter_horizontal = ()
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'nickname',)}),
    )

    add_fieldsets = (
        ("User Details", {'fields': ('email', 'password', 'password2',)}),
    )
