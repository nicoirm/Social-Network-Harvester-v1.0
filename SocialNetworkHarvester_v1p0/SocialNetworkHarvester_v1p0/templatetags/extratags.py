from django import template
from collections import OrderedDict
from Twitter.models import TWUser,Hashtag,Tweet,TWPlace, favorite_tweet, follower, HashtagHarvester
from Youtube.models import YTChannel, YTVideo, YTPlaylist, YTPlaylistItem, YTComment
from Facebook.models import FBUser, FBPage, FBPost, FBComment,FBReaction
import re

register = template.Library()


from SocialNetworkHarvester_v1p0.settings import viewsLogger, DEBUG, STATICFILES_VERSION, FACEBOOK_APP_PARAMS

log = lambda s: viewsLogger.log(s) if DEBUG else 0
pretty = lambda s: viewsLogger.pretty(s) if DEBUG else 0

@register.filter
def sort(value):
    return sorted(value)

@register.filter
def getFields(className):
    '''Get the name and description of each relevant (downloadable) field of a given Aspira object.
    Use inside a template with:
    {% for key,val in 'className'|getFields %} ... {% endfor %}
    In order to work, the method "get_fields_description" should be implemented in the model
    :param className: The Class name of a given model. (example: "TWUser", "TWeet". "Hashtag", etc.)
    :return: a list of tuples, containing a string (field) and a dict {"name":"aName","description":"aDescription"}.
    '''
    fields = globals()[className]().get_fields_description()
    keys = fields.keys()
    orderedFields = []
    for key in sorted(keys):
        orderedFields.append((key,fields[key]))
    return orderedFields


@register.filter
def getFieldsAsDict(className):
    fields = globals()[className]().get_fields_description()
    return fields


@register.filter
def join(string, arg):
    '''
    :param string: The string to be appended
    :return: joit string and args values
    '''
    return re.sub(" ","_", str(string) + str(arg))


@register.filter
def multiply(a, b):
    return a * b