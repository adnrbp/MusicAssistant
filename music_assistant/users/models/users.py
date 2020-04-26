"""User models."""

# Django
from django.db import models

class User(models.Model):
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    remote_id = models.CharField(
            "sender_id", 
            max_length=20,
            unique=True
        )

    @classmethod
    def register_new_user(cls, sender_id, user_name, last_name):
        return cls.objects.get_or_create(
                    remote_id=sender_id,
                    first_name=user_name,
                    last_name=last_name
                )
    @classmethod
    def get_user_by_sender_id(cls,sender_id):
        try:
            user = cls.objects.get(remote_id=sender_id)
        except User.DoesNotExist:
            user = None
        return user