"""
App-level settings
"""
from django.conf import settings

FB_VERIFY_TOKEN = settings.FACEBOOK_VERIFY_TOKEN
FB_ACCESS_TOKEN = settings.FACEBOOK_ACCESS_TOKEN

FB_ACCESS_TOKEN_PARAM = {
    'access_token': FB_ACCESS_TOKEN
}