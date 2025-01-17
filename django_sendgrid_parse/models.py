import os
import re
import hashlib

from django.db import models
from jsonfield import JSONField

from . import _ugl


def attachments_file_upload(instance, filename):
    fn, ext = os.path.splitext(filename)

    emails = instance.email.to_mailbox.split(',')
    emails_sanitized = ["_".join(filter(None, re.split(r'\W+', email)))[:10] for email in emails]
    emails_hashed = hashlib.md5("_".join(emails_sanitized).encode('utf-8')).hexdigest()

    return 'emails/{to}/{id}/{fn}{ext}'.format(
        to=emails_hashed,
        id=instance.email.id,
        fn=fn[:25],
        ext=ext
    )


class Email(models.Model):
    headers = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('Headers')
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('Text')
    )
    html = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('HTML')
    )
    to_mailbox = models.TextField(
        verbose_name=_ugl('To')
    )
    from_mailbox = models.TextField(
        verbose_name=_ugl('From')
    )
    cc = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('Carbon Copy')
    )
    subject = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('Subject')
    )
    # Changed because sendgrid doesn't respect REST and JSON standards ¬¬
    dkim = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('DomainKeys Identified Mail')
    )
    # Changed because sendgrid doesn't respect REST and JSON standards ¬¬
    SPF = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('Sender Policy Framework')
    )
    envelope = JSONField(
        default={'to': None, 'from': None},
        blank=True,
        null=True,
        verbose_name=_ugl('Envelope')
    )
    charsets = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_ugl('Charsets')
    )
    spam_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_ugl('Spam score')
    )
    spam_report = models.TextField(
        blank=True,
        null=True,
        verbose_name=_ugl('Spam report')
    )
    creation_date = models.DateTimeField(
       auto_now_add=True,
       verbose_name=_ugl('Creation date')
    )
    content_ids = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_ugl('Content ids')
    )
    sender_ip = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_ugl('Sender ip')
    )
    attachment_info = JSONField(
        blank=True,
        null=True,
        verbose_name=_ugl('Attachment Info')
    )

    def __str__(self):
        return f"Email from '{self.from_mailbox}' to '{self.to_mailbox}' with subject '{self.subject}'"


class Attachment(models.Model):
    number = models.IntegerField(
        default=1,
        verbose_name=_ugl("Email's Attachment Number")
    )
    file = models.FileField(
        upload_to=attachments_file_upload,
        verbose_name=_ugl('Attached File'),
        max_length=1000,
    )
    email = models.ForeignKey(
        Email,
        on_delete=models.deletion.CASCADE,
        related_name='attachments',
        verbose_name=_ugl("Email Attached To")
    )

    @property
    def filename(self):
        return os.path.basename(self.file.name)
