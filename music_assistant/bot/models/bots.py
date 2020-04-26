""" Bot utility model. """

#Django
from django.db import models

class BotModel(models.Model):
    """ Bot base model.
    BotModel acts as an abstract base class from which every
    other model in Bot app will inherit. 
    The following attributes will be provided:
        + created (DateTime): Store the creation time of the object.
    """

    created = models.DateTimeField(
        'created at', 
        auto_now_add=True,
        help_text='Date time of the object creation'
    )

    class Meta:
        abstract = True
        #get_latest_by = 'created'
        #ordering = ['-created', '-modified']