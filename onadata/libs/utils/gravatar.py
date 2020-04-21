# coding: utf-8
from __future__ import unicode_literals, print_function, division, absolute_import

import hashlib
import urllib

DEFAULT_GRAVATAR = "https://formhub.org/static/images/formhub_avatar.png"
GRAVATAR_ENDPOINT = "https://secure.gravatar.com/avatar/"
GRAVATAR_SIZE = str(60)


def get_gravatar_img_link(user):
    url = GRAVATAR_ENDPOINT +\
        hashlib.md5(user.email.lower().encode()).hexdigest() + "?" + urllib.urlencode({
            'd': DEFAULT_GRAVATAR, 's': GRAVATAR_SIZE
        })
    return url


def gravatar_exists(user):
    url = GRAVATAR_ENDPOINT +\
        hashlib.md5(user.email.lower().encode()).hexdigest() + "?" + "d=404"
    exists = urllib.urlopen(url).getcode() != 404
    return exists
