from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ["pkid", "title", "content", "author"]
        read_only_fields = ("pkid", "author")

    def get_author(self, obj):
        return obj.author.full_name
