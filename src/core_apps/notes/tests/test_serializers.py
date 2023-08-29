import pytest
from django.test import TestCase

from ..serializers import NoteSerializer


def get_fields_list():
    return ["pkid", "title", "content", "author"]


@pytest.mark.usefixtures("note", "user")
class NoteTests(TestCase):
    def setUp(self):
        self.serializer_data = {
            field: getattr(self.note, field) for field in get_fields_list()
        }
        self.serializer = NoteSerializer(instance=self.note)

    def test_note_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(get_fields_list()))

    def test_note_serializer_author_is_user_full_name(self):
        self.assertEqual(self.serializer.data["author"], self.note.author.full_name)
