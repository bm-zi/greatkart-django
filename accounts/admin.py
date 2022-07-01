from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile

from .models import UserProfile
from django.utils.html import format_html


# class UserAdmin that encapsulates all admin options and 
# functionality for a given model.

class AccountAdmin(UserAdmin):
    # control which fields are displayed
    list_display = ('email', 'first_name', 'last_name', 
        'username', 'last_login', 'date_joined', 'is_active'
    )

    # control which fields in list_display should be linked
    list_display_links = ('email', 'first_name', 'last_name')


    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()  # display horizontal
    
    # No filters in the right sidebar of the change list page of the admin
    list_filter = ()

    # Set fieldsets to control the layout of admin “add” and “change” pages.
    fieldsets = () 


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)