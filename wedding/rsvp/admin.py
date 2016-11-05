from django.contrib import admin
from .models import Person, Invitation


class PersonAdmin(admin.TabularInline):
    model = Person


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('title', 'zip_code')
    inlines = (PersonAdmin,)

admin.site.register(Invitation, InvitationAdmin)
admin.site.site_header = 'Wedding Admin'
