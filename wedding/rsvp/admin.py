from django.contrib import admin
from .models import Person, Invitation
from import_export import resources
from import_export.admin import ExportMixin


class PersonResource(resources.ModelResource):
    """Resource for export tool"""

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'responded', 'responded_datetime',
                  'coming',)


class PersonAdmin(ExportMixin, admin.ModelAdmin):
    model = Person
    list_display = ('first_name', 'last_name', 'responded', 'coming',)
    resource_class = PersonResource


class TabularPersonAdmin(admin.TabularInline):
    model = Person
    fields = ('first_name', 'last_name', 'display_name', 'coming', 'responded',)


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('title', 'zip_code',)
    inlines = (TabularPersonAdmin,)


admin.site.register(Person, PersonAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.site_header = 'Wedding Admin'
