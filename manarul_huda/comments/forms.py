from django import forms
from django_comments.forms import CommentDetailsForm
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

class CustomCommentForm(CommentDetailsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("url")
        
    def _get_client_ip(self):
        if self.request:
            ip_address = self.request.META.get('REMOTE_ADDR', '')
            return ip_address
        return ''

    def get_comment_create_data(self, site_id=None):
        return dict (
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk = self.target_object.pk,
            name = self.cleaned_data["name"],
            email = self.cleaned_data["email"],
            comment = self.cleaned_data["comment"],
            submit_date = timezone.now(),
            site_id = site_id or getattr(settings, "SITE_ID", None),
            is_public = False,
            is_removed = False,
        )
    