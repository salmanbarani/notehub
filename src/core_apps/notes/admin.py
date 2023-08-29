from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "title", "author"]
    list_display_links = ["id", "pkid"]


admin.site.register(Note, NoteAdmin)
