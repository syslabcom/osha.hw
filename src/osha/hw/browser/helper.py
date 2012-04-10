from Acquisition import aq_inner
from OFS.Image import File
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.Five import BrowserView
from zope.component import getUtility

from logging import getLogger
log = getLogger('osha.hw helper')

IEXT = ('gif', 'jpg', 'png')

class GetThumb(BrowserView):

    def __call__(self):
        """ return a sensible thumb"""
        placeholder_url = '/_themes/hw2012/Media/placeholder.png'
        obj = aq_inner(self.context)
        now = DateTime()
        yesterday = now-1
        
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        response = self.request.RESPONSE
        response.setHeader('Last-Modified', yesterday.ISO())
        response.setHeader('Cache-Control', 'max-age=86400, proxy-revalidate, public')
        
        myid = obj.getId()
        if '.' in myid:
            elems = myid.split('.')
            stem = '.'.join(elems[0:-1])
        else:
            stem = myid
#        import pdb; pdb.set_trace()
        siblings = obj.aq_parent.objectIds()
        imgid = ''
        for sibling in siblings:
            if sibling.startswith(stem):
                for ext in IEXT:
                    if "%s.%s" %(stem, ext) == sibling:
                        imgid = "%s.%s" %(stem, ext)
                        break
        if imgid:
            thumb_url = "%s/%s" %(obj.aq_parent.absolute_url(), imgid)
            return response.redirect(thumb_url, status=301)

        return response.redirect(placeholder_url, status=302)
