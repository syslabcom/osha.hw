import logging
import simplejson as json

from zope.interface import implements
from zope.i18n import translate

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.Archetypes import PloneMessageFactory as _
from ZPublisher import HTTPResponse


class NewsByPathView(BrowserView):
    """ When called with a counter, it renders a news so that it fits into 
    the homepage box """
    index = ViewPageTemplateFile("templates/news_by_path.pt")
    
    def __call__(self):
        no = int(self.request.get('no', 1))
        # careful, no is repeat/news/number, so 1..n, not 0..n-1
        helper = self.context.restrictedTraverse('@@hw_view')
        self.news = [x for x in helper.getNews(limit=3, strip_links=1)]
        self.newsfolder_url = helper.getNewsfolderUrl()
        if 0 < no < 4:
            self.current_news = self.news[no-1]
        else:
            self.current_news = {}
        return self.index(self)


class EventByPathView(BrowserView):
    """ When called with a path, it renders a news so that it fits into the homepage box """
    index = ViewPageTemplateFile("templates/event_by_path.pt")
    
    def __call__(self):
        no = int(self.request.get('no', 1))
        # careful, no is repeat/news/number, so 1..n, not 0..n-1
        helper = self.context.restrictedTraverse('@@hw_view')
        events = [x for x in helper.getEvents(limit=3)]
        if 0<no<4:
            self.event = events[no-1]
        else:
            self.event = {}
        return self.index(self)
            
