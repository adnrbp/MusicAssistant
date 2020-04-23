""" Messages Logic """

# Helpers
from .fb_messages import FbMessageAPI

class Handlers():
    """ Handle messages and Build Responders"""

    @classmethod
    def facebook_message(cls, sender_id, recevied_message):
        """ 
        Create an instance of FB Message Response Builder and handle its response
        """
        fb = FbMessageAPI(sender_id)
        fb.text_message(recevied_message)