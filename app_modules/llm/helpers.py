from random import randrange

from django.core.cache import cache

from base import constants


def get_user_cache_key(chat_bot_type, user):
    return constants.LLMConstants.CACHE_KEYS[chat_bot_type].format(user_id=user.id)


def delete_user_cache_key(cache_key):
    cache.delete(cache_key)


def random_number():
    return randrange(100000, 999999)
