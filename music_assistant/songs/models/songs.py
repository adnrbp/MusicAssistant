"""Song models."""

# Django
from django.db import models
from django.db.models import Count


class Song(models.Model):
    name = models.CharField("track name", max_length=100)
    artist_name = models.CharField("artist name", max_length=50)
    remote_id = models.CharField(
            "track_id", 
            max_length=15,
            unique=True
        )

    @classmethod
    def get_track(cls,track_id):
        try:
            track = cls.objects.get(remote_id=track_id)
        except Song.DoesNotExist:
            track = None
        return track

    @classmethod
    def save_track(cls,name, artist,track_id):
        new_track = cls.objects.create(
                name=name,
                artist_name=artist,
                remote_id= track_id
            )
        return new_track


    @classmethod
    def favorites_by_user(cls, sender_id):
        """search all favorite songs of a user"""
        songs = cls.objects.filter(favorited_by_users__user__remote_id=sender_id).values()

        return list(songs)

    @classmethod
    def get_top_songs(cls):
        songs = cls.objects
        favorites_per_song = songs.annotate(favorited_by_users_count=Count('favorited_by_users'))
        top_songs = favorites_per_song.order_by('-favorited_by_users_count')[:5].values()
        return list(top_songs)
