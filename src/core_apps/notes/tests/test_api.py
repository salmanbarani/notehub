import pytest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core_apps.users.factories import UserFactory
from ..models import Note

PAGE_SIZE = 5
NOTE_URL = "/api/v1/notes"


def get_payload(user, title="title", content="content"):
    return {"author": user, "title": title, "content": content}


def add_notes_to_user(user, size=3):
    for note in Note.objects.all()[:3]:
        note.author = user
        note.save()
    return Note.objects.filter(author=user).count()


@pytest.mark.usefixtures("user", "note", "notes", "user_note")
class NotesApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_list_of_notes(self):
        user_notes_size = 3
        add_notes_to_user(self.user, user_notes_size)
        response = self.client.get(NOTE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), user_notes_size)

    def test_get_note_detail(self):
        note_id = self.user_note.pkid
        response = self.client.get(f"{NOTE_URL}{note_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        note_title = self.user_note.title
        response_title = response.json()["title"]
        self.assertEqual(note_title, response_title)

    def test_publish_not_authenticated_note(self):
        response = APIClient().get(NOTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_plublish_note_mission_data(self):
        payload = get_payload(self.user, title="")
        response = self.client.post(NOTE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_note(self):
        payload = get_payload(self.user)
        payload.pop("author")

        response = self.client.post(NOTE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], response.json()[key])
        self.assertEqual(self.user.full_name, response.json()["author"])

    def test_unpublish_not_owner_book(self):
        client = APIClient()
        client.force_authenticate(UserFactory())
        response = client.delete(f"{NOTE_URL}{self.user_note.pkid}/")  # the actual author is self.user
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book(self):
        response = self.client.delete(f"{NOTE_URL}{self.user_note.pkid}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_not_owner_book(self):
        client = APIClient()
        client.force_authenticate(UserFactory())
        response = client.patch(f"{NOTE_URL}{self.user_note.pkid}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_success(self):
        payload = get_payload(self.user)
        payload['title'] = "title-was-updated"
        response = self.client.patch(f"{NOTE_URL}{self.user_note.pkid}/", data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['title'], response.json()['title'])

    def test_search_by_filter(self):
        user_books = add_notes_to_user(self.user)
        filter_fields = {
            "format": "json",
            "author__first_name": self.user.first_name,
            "author__last_name": self.user.last_name,
        }
        response = self.client.get(NOTE_URL, filter_fields)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), user_books)
