#
# gravatars.py -- Decorational template tags
#
# Copyright (c) 2008-2009  Christian Hammond
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

from django import template
from django.utils.html import format_html

from djblets.gravatars import (get_gravatar_url,
                               get_gravatar_url_for_email)
from djblets.util.decorators import basictag


register = template.Library()


@register.tag
@basictag(takes_context=True)
def gravatar(context, user, size=None):
    """Output the HTML for displaying a user's Gravatar.

    This can take an optional size of the image (defaults to 80 if not
    specified).

    This is also influenced by the following settings in :file:`settings.py`:

    ``GRAVATAR_SIZE``:
        Default size for Gravatars.

    ``GRAVATAR_RATING``:
        Maximum allowed rating. This should be one of: ``g``, ``pg``, ``r``,
        ``x``

    ``GRAVATAR_DEFAULT``:
        Default image set to show if the user hasn't specified a Gravatar.
        This should be one of: ``identicon``, ``monsterid``, ``wavatar``

    See https://www.gravatar.com/ for more information.

    Args:
        context (django.template.RequestContext):
            The context for the page.

        user (django.contrib.auth.models.User):
            The user for the Gravatar.

        size (int, optional):
            The size of the Gravatar. Defaults to 80.

    Returns:
        unicode:
        The HTML for displaying the Gravatar.
    """
    url = get_gravatar_url(context['request'], user, size)

    if url:
        return format_html(
            '<img src="{0}" width="{1}" height="{1}" alt="{2}" '
            'class="gravatar"/>',
            url, size, user.get_full_name() or user.username)
    else:
        return ''


@register.tag
@basictag(takes_context=True)
def gravatar_url(context, email, size=None):
    """Output the URL for a Gravatar for the given email address.

    This can take an optional size of the image (defaults to 80 if not
    specified).

    This is also influenced by the following settings in :file:`settings.py`:

    ``GRAVATAR_SIZE``:
        Default size for Gravatars.

    ``GRAVATAR_RATING``:
        Maximum allowed rating. This should be one of: ``g``, ``pg``, ``r``,
        ``x``

    ``GRAVATAR_DEFAULT``:
        Default image set to show if the user hasn't specified a Gravatar.
        This should be one of: ``identicon``, ``monsterid``, ``wavatar``

    See https://www.gravatar.com/ for more information.

    Args:
        context (django.template.RequestContext):
            The context for the page.

        email (unicode):
            The e-mail address for the user.

        size (int, optional):
            The size of the Gravatar. Defaults to 80.

    Returns:
        unicode:
        The HTML for displaying the Gravatar.
    """
    return get_gravatar_url_for_email(context['request'], email, size)
