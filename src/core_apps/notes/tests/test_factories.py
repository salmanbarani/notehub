import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..factories import NoteFactory
from ..models import Note

User = get_user_model()


@pytest.mark.usefixtures("note", "user")
class NoteFactoryTestCase(TestCase):
    def test_note_factory(self):
        self.assertTrue(Note.objects.filter(pkid=self.note.pkid))

    def test_book_factory_sequence(self):
        NoteFactory.create_batch(size=4)
        self.assertEqual(Note.objects.count(), 5)  # 4 + 1 (in conftest file)
