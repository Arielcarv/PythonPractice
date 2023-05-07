import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="playground", permanent=False)),
    path("playground/", include("playground.urls")),
    path("store/", include("store.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]
