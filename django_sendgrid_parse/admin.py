from django.contrib import admin
from django.utils.html import format_html

from . import models


class AttachentAdminInline(admin.TabularInline):
    model = models.Attachment


class EmailAdmin(admin.ModelAdmin):
    inlines = [
        AttachentAdminInline
    ]
    list_display = ('display_from_mailbox', 'display_to_mailbox', 'subject', 'creation_date')
    search_fields = ('from_mailbox', 'to_mailbox', 'subject')

    def display_from_mailbox(self, obj):
        return obj.from_mailbox
    display_from_mailbox.short_description = 'From'

    def display_to_mailbox(self, obj):
        return format_html(
            '<span title="{}">{}</span>',
            obj.to_mailbox,
            obj.to_mailbox[:50] + '...' if len(obj.to_mailbox) > 50 else obj.to_mailbox
        )
    display_to_mailbox.short_description = 'To'


admin.site.register(models.Attachment)
admin.site.register(models.Email, EmailAdmin)
