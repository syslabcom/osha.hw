from Acquisition import aq_inner
from OFS.Image import File
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.Five import BrowserView
from zope.component import getUtility
from zope.interface import implements
from osha.hw.interfaces import IHelperView
from slc.subsite.root import getSubsiteRoot

from logging import getLogger
log = getLogger('osha.hw helper')

IEXT = ('gif', 'jpg', 'png')
TOPLEVELFOLDERS = ('about', 'get-involved', 'leadership', 'media', 'resources', 'worker-participation')


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



class HelperView(BrowserView):
    """ Helper View to manage the campaign site setup """
    implements(IHelperView)

    def __init__(self, context, request=None):
        self.context = context
        self.ltool = getToolByName(context, 'portal_languages')
        self.pref_lang = self.ltool.getPreferredLanguage()
        self.supported_langs = self.ltool.getSupportedLanguages()
        self.available_langs = self.ltool.getAvailableLanguages()
        self.subsite_path = getSubsiteRoot(aq_inner(context))

    def getTranslations(self):
        langinfo = self.ltool.getAvailableLanguageInformation()
        translations = self.context.getTranslations()
        langs = translations.keys()
        langs.sort()
        for lang in langs:
            if lang not in self.available_langs:
                continue
            obj = translations[lang][0]
            info = langinfo.get(lang, None)
            native = info is not None and info.get('native', lang) or lang
            yield dict(obj=obj, lang=lang, native=native)

    def getNavigation(self):
        root = self.context.restrictedTraverse(self.subsite_path)
        langroot = getattr(root, self.pref_lang, getattr(root, 'en'))
        landing_pages = [x.getObject() for x in langroot.getFolderContents( \
        {'portal_type':'Folder'})]
        landing_pages = [x for x in landing_pages if not x.getExcludeFromNav()]
        for landing_page in landing_pages:
            detail_pages = landing_page.getFolderContents({'portal_type':  'Folder'})
            yield (landing_page, detail_pages)

    def getHomeURL(self):
        # hardcoded for the moment
        return "http://hw2012.syslab.com"

    def set_views(self):
        """ sets the views on all folders """
        # make sure we are called on the campaign root folder
        assert (self.context.getId()=='hw2012')
        msg = "HW Helper - set_views\n====================\n\n"
        for lang in self.supported_langs:
            msg += "LANGUAGE: %s\n============\n\n" % lang.upper()

            if not hasattr(self.context.aq_explicit, lang):
                continue

            langfolder = getattr(self.context, lang, None)
            if not langfolder:
                continue
            for toplevel in TOPLEVELFOLDERS:
                if hasattr(langfolder.aq_explicit, toplevel):
                    toplevelfolder = getattr(langfolder, toplevel, None)
                    msg += self._sp(toplevelfolder, 'layout', 'hw2012_landing_page')


                    for sub in toplevelfolder.objectValues('ATFolder'):
                        dv = sub.getDefaultPage()
                        if dv in sub.objectIds():
                            msg += self._sp(getattr(sub, dv), 'layout', 'hw2012_details_page')
                        else:
                            msg += self._sp(sub, 'layout', 'hw2012_details_page')

        self.request.RESPONSE.setHeader('Content-type', 'text/plain')
        return msg


    def _sp(self, ob, id, value, type="string"):
        """ simple set property. Checks if present """
        msg = ""
        XX = ob.getProperty(id)
        if XX.startswith('hw2012_'):
            msg += "Skipping %s, preserving already set\n" % ob.absolute_url(1)
            return msg
            
        if not ob.hasProperty(id):
            ob._setProperty(id, value, type)
            msg+=".. set new layout property: %s\n" % ob.absolute_url(1)
        else:
            ob._updateProperty(id, value)
            msg+=".. update layout property: %s\n" % ob.absolute_url(1)
        return msg


