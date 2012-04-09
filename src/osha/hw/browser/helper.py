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
        placeholder_url = '/_themes/Media/placeHolder.png'
        obj = self.context
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
        
        siblings = obj.aq_parent.objectIds()
        imgid = ''
        for sibling in siblings:
            if sibling.startswith(stem):
                for ext in IEXT:
                    imgid = "%s.%s" %(stem, ext)
                    if imgid == sibling:
                        break
        if imgid:
            thumb_url = "%s/%s/hwsmall" %(obj.aq_parent.absolute_url(), imgid)
            return response.redirect(thumb_url, status=301)

        return response.redirect(placeholder_url, status=302)
