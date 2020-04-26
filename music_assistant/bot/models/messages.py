"""Conversation message models."""

# Django
from django.db import models

# Utilities
from .bots import BotModel

class Message(BotModel):
    """ Conversation Message.
    A conversation message represents an interaction 
    between a user the bot within a conversation.
    """

    conversation = models.ForeignKey(
        'bot.Conversation', 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.CharField('message content',max_length=50)
    is_postback = models.BooleanField(default=False)
    #author = models.CharField("writter", max_length=50) # bot or user

    @classmethod
    def save_text(cls,conversation,response_data,is_postback=False):
        cls.objects.create(
                conversation=conversation,
                content=response_data,
                is_postback=is_postback
                )