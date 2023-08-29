from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .pagination import NotePagination
from .serializers import NoteSerializer


class NoteOwnershipMixin(viewsets.ModelViewSet):
    def check_ownership(self, note, request):
        if note.author == request.user:
            return True
        raise PermissionDenied("note doesn't belong to you")


class NoteViewSet(NoteOwnershipMixin):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = NotePagination
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "title": ["exact", "icontains"],
        "author__first_name": ["exact", "icontains"],
        "author__last_name": ["exact", "icontains"],
    }

    def get_queryset(self):
        queryset = self.queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        self.check_ownership(self.get_object(), request)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.check_ownership(self.get_object(), request)
        return super().update(request, *args, **kwargs)
