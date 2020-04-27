"""User Conversation models."""

# Django
from django.db import models
from django.db.models import Count

# Model Utilities
from .bots import BotModel

# Utilities
from datetime import datetime, timedelta, timezone

class Conversation(BotModel):

    last_interaction = models.DateTimeField('updated at', 
        auto_now=True,
        help_text='Date time of the last user message'
    )
    has_interaction = models.BooleanField('multi-message', default=False)
    last_postback = models.CharField(
        max_length=50,
        help_text='stores last postback message to speed interactions',
        default= ''
    )
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE,
        help_text='Interacts with bot and make requests',
        related_name='conversations'
    )

    @classmethod
    def register_new_conversation(cls,user):
        # multiple conversations in a day
        # get last conversation of the day in range of 2h
        recent_conversation = cls.objects.filter(user=user).last()
        # more than 2 hours of last_interaction?
        if recent_conversation is not None:
            last_time = recent_conversation.last_interaction 
            now = datetime.now(timezone.utc)
            if (now - last_time) > timedelta(hours=2):
                # yes: create new conversation
                new_conversation = cls.objects.create(user=user)
                return new_conversation.id
            else:
                # no: return that last conversation
                return recent_conversation.id
        else:
            new_conversation = cls.objects.create(user=user)
            return new_conversation.id
            
    @classmethod
    def get_last_message(cls, conversation_id): #sender_id):
        """Check if the las message is a postback"""
        #last_conversation = Conversation.objects.filter(user__remote_id=sender_id).last()
        last_conversation = Conversation.objects.filter(id=conversation_id).last()
        last_message = last_conversation.messages.last()
        if last_message is not None:
            follow_up_saved_with_postback = last_message.is_postback
            payload = last_message.conversation.last_postback
        else:
            follow_up_saved_with_postback = False
            payload = ""
        return (last_conversation, follow_up_saved_with_postback, payload)

    @classmethod
    def set_postback(cls, conversation_id, postback_payload):
        conversation = cls.objects.get(id=conversation_id)
        conversation.last_postback = postback_payload
        conversation.save(update_fields=["last_postback"])
        return conversation

    @classmethod
    def quantity_by_day(cls):
        chats_per_day = cls.objects.extra(select={'day': 'date( created )'}) \
                            .values('day') \
                            .annotate(chats=Count('created'))
        chats_daily_quantity = cls.objects.count() // len(chats_per_day)
        return chats_daily_quantity