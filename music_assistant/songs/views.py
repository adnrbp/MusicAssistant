""" Songs views. """

from django.views.generic import TemplateView

class SongView(TemplateView):
    template_name = "songs/home.html"
