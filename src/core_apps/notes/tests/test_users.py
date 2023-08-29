from decimal import Decimal
import pytest
from django.test import TestCase


@pytest.mark.usefixtures("note")
class NoteTests(TestCase):
    def test_note_is_created(self):
        self.assertEqual(str(self.note), self.note.title)
