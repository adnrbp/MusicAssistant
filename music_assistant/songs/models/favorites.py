"""User Favorite Songs models."""

# Django
from django.db import models

class Favorite(models.Model):
    song = models.ForeignKey(
        "songs.Song", 
        on_delete=models.CASCADE,
        related_name="favorited_by_users")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="favorite_songs")

    @classmethod
    def user_already_saved(cls,user, song):
        try:
            favorite_record = cls.objects.get(user=user, song=song)
        except cls.DoesNotExist:
            favorite_record = None
        return favorite_record

    @classmethod
    def save_track(cls,user, song):
        result = False
        if cls.user_already_saved(user, song) is None:
            cls.objects.create(user=user,song=song)
            result = True
        return result

