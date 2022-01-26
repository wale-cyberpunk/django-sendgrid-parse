from django.contrib import admin

from . import models


class AttachentAdminInline(admin.TabularInline):
    model = models.Attachment


class EmailAdmin(admin.ModelAdmin):
    inlines = [
        AttachentAdminInline
    ]


admin.site.register(models.Attachment)
admin.site.register(models.Email, EmailAdmin)
