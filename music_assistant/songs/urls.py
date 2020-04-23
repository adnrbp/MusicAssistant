
from django.urls import path

from .views import SongView

urlpatterns = [
    path("", SongView.as_view(), name="home"),
]
