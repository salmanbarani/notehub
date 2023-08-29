import pytest
from django.conf import settings
from core_apps.users.factories import UserFactory
from .. import factories


@pytest.fixture(scope="class")
def user(request):
    request.cls.user = UserFactory()


@pytest.fixture(scope="class")
def note(request):
    request.cls.note = factories.NoteFactory()


@pytest.fixture(scope="class")
def user_note(request):
    request.cls.user_note = factories.NoteFactory(author=request.cls.user)


@pytest.fixture(scope="class")
def notes(request):
    factories.NoteFactory.create_batch(size=30)
