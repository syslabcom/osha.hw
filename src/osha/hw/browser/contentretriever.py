import logging
import simplejson as json

from zope.interface import implements
from zope.i18n import translate

from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Archetypes import PloneMessageFactory as _
from ZPublisher import HTTPResponse

class NewsByPathView(BrowserView):
    """ When called with a path, it renders a news so that it fits into the homepage box """
    