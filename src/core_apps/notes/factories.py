import factory
from django.conf import settings
from faker import Faker

from .models import Note

fake = Faker()


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Sequence(lambda n: f"Title {n}")
    content = factory.Faker("paragraph")
    author = factory.SubFactory(settings.AUTH_USER_FACTORY)
