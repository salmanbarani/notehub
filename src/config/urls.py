from django.conf import settings
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="NoteHub API",
        default_version="v1",
        description="API endpoints for the NoteHub platform",
        contact=openapi.Contact(email="salmanandb@outlook.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/notes", include("core_apps.notes.urls")),

]


admin.site.site_header = "NoteHub API Admin"
admin.site.site_title = "NoteHub API Admin Portal"
admin.site.index_title = "Welcome to the NoteHub API Portal"
