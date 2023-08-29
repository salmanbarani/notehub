from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Note(TimeStampedUUIDModel):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    content = models.TextField(verbose_name=_("content"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes", verbose_name=_("author"))

    def __str__(self):
        return self.title
