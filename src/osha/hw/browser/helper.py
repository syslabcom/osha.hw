from Acquisition import aq_inner, aq_parent
from OFS.Image import File
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.Five import BrowserView
from zope.component import getUtility
from zope.interface import implements
from osha.hw.interfaces import IHelperView
from slc.subsite.root import getSubsiteRoot
from osha.policy.utils import logit
from osha.hw.browser.sync_receiver import BaseDBView
from osha.hw.queries import insert_hw2012_charter, create_hw2012_charter
from osha.hw.util import generatePDF, send_charter_email
from zope.i18n import translate

from logging import getLogger
log = getLogger('osha.hw helper')

IEXT = ('gif', 'jpg', 'png')
TOPLEVELFOLDERS = ('about', 'get-involved', 'leadership', 'media', 'resources', 'worker-participation')
SV = {
    'news': 'hw2012_news',
    'events': 'hw2012_events',
    
    'leadership': 'hw2012_landing_page',
    'leadership/leadership': 'hw2012_landing_page',
    'leadership/benefits/benefits': 'hw2012_details_page',
    'leadership/enterprises-survey/enterprises-survey': 'hw2012_details_page',
    'leadership/leadership-guide/leadership-guide': 'hw2012_details_page',
    'leadership/leadership-self-assessment/leadership-checklist': 'hw2012_details_page',
    'leadership/legislation/legislation': 'hw2012_details_page',

    'worker-participation': 'hw2012_landing_page',
    'worker-participation/worker-participation': 'hw2012_landing_page',
    'worker-participation/benefits/benefits': 'hw2012_details_page',
    'worker-participation/enterprises-survey/enterprises-survey': 'hw2012_details_page',
    'worker-participation/worker-participation-guide/worker-participation-guide': 'hw2012_details_page',
    'worker-participation/worker-participation-checklist/worker-participation-checklist': 'hw2012_details_page',
    'worker-participation/legislation/legislation': 'hw2012_details_page',
    
    'media': 'hw2012_landing_page',
    'media/media': 'hw2012_landing_page',
    'media/press/press': 'hw2012_press_press_template',
    'media/photo-gallery': 'hw2012_image_folders',
    'media/napo-film': 'hw2012_details_page',
    
    'resources': 'hw2012_landing_page',
    'resources/resources': 'hw2012_landing_page',
    'resources/case-studies/case-studies': 'hw2012_details_page',
    'resources/publications': 'hw2012_resources_publications_html',
    'resources/preventive-solutions/preventive-solutions': 'hw2012_details_page',
    'resources/practical-tools/practical-tools': 'hw2012_details_page',
    'resources/oira/oira': 'hw2012_details_page',
    'resources/campaign-essentials': 'hw2012_resources_campaignessentials_html',
    'resources/promotion-materials': 'hw2012_resources_promotionalmaterials_html',
    'resources/napo-film/napo-film': 'hw2012_details_page',
    
    'about': 'hw2012_landing_page',
    'about/about': 'hw2012_landing_page',
    'about/about_the_campaign/about-the-campaign': 'hw2012_details_page',
    'about/campaign-partners/campaign-partners': 'hw_ocps',
    'about/focal-points/focal-points': 'hw_fops',
    'about/enterprise-europe-network/enterprise-europe-network': 'hw2012_details_page',

    'get-involved': 'hw2012_landing_page',
    'get-involved/get-involved': 'hw2012_landing_page',
    'get-involved/how_to_get_involved/how-to-get-involved': 'hw2012_details_page',
    'get-involved/good-practice-award/good-practice-award': 'hw2012_details_page',
    'get-involved/become-a-eu-partner/become-a-eu-partner': 'hw2012_details_page',
    'get-involved/become-a-national-partner/become-a-national-partner': 'hw2012_details_page',
    'get-involved/european-week/european-week': 'hw2012_details_page',

}


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
        self.ptool = getToolByName(context, 'portal_url')
        self.ltool = getToolByName(context, 'portal_languages')
        self.pref_lang = self.ltool.getPreferredLanguage()
        self.supported_langs = self.ltool.getSupportedLanguages()
        self.available_langs = self.ltool.getAvailableLanguages()
        self.subsite_path = getSubsiteRoot(aq_inner(context))
        self.root = self.context.restrictedTraverse(self.subsite_path)
        self.langroot = getattr(self.root, self.pref_lang, getattr(self.root, 'en'))

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
        landing_pages = [x.getObject() for x in self.langroot.getFolderContents( \
        {'portal_type':'Folder'})]
        landing_pages = [x for x in landing_pages if not x.getExcludeFromNav()]
        for landing_page in landing_pages:
            detail_pages = landing_page.getFolderContents({'portal_type':  'Folder'})
            yield (landing_page, detail_pages)

    def getHomeURL(self):
        # hardcoded for the moment
        return "http://www.healthy-workplaces.eu/"

    def getNewsfolderUrl(self):
        return self.langroot.restrictedTraverse('news').absolute_url()

    def getEventsfolderUrl(self):
        return self.langroot.restrictedTraverse('events').absolute_url()

    def getSlogan(self):
        """ Fetches the translated slogan text """
        # id = self.langroot.getDefaultPage()
        # doc = getattr(self.langroot, id)
        # return doc.getText()
        slogan = translate('campaign_slogan_2012', domain="osha_ew",
            target_language=self.pref_lang)
        return slogan

    def getNews(self, limit=0):
        """Fetch campaign-related News and return the relevant parts"""
        subject = aq_inner(self.root).Subject()
        portal_path = self.ptool.getPortalPath()
        lang = self.context.portal_languages.getPreferredLanguage()
        pc = getToolByName(self.context, 'portal_catalog')
        res = pc(portal_type='News Item',
            Language=['en', ''],
            sort_order='reverse', sort_on='effective',
            expires={'query': DateTime(), 'range': 'min'},
            path=['%s/en' % portal_path, '%s/%s' % (portal_path, self.pref_lang),
            self.subsite_path],
            Subject=subject)
        if len(res) and limit > 0:
            res = res[:limit]
        for r in res:
            obj = r.getObject()
            # now get the correct translation, or use the EN one as fallback
            obj = obj.getTranslation(self.pref_lang) or obj
            link = "%s/@@hw.telescope?path=%s" % (self.getNewsfolderUrl(), r.getPath())
            img_url = obj.getImage() and '/'.join(obj.getImage().getPhysicalPath()) or ''
            img_url = img_url.replace('/osha/portal', 'https://osha.europa.eu')
            description = obj.Description().strip() != '' and obj.Description() or obj.getText()
            date = obj.effective()
            yield dict(link=link, img_url=img_url, description=description,
                title=obj.Title(), day=date.day(), month=date.pMonth(), year=date.year())

    def getEvents(self, limit=0):
        """Fetch campaign-related Events and return the relevant parts"""
        subject = aq_inner(self.root).Subject()
        portal_path = self.ptool.getPortalPath()
        pc = getToolByName(self.context, 'portal_catalog')
        res = pc(portal_type='Event',
            Language=['en', ''],
            sort_order='reverse', sort_on='start',
            end={'query': DateTime(), 'range': 'min'}, expires={'query': DateTime(), 'range': 'min'},
            path=['%s/en' % portal_path, '%s/%s' % (portal_path, self.pref_lang),
            self.subsite_path],
            Subject=subject)
        if len(res) and limit > 0:
            res = res[:limit]
            
        if len(res)==0:
            now = DateTime()
            yield dict(link='', location='', start=now, description='There are currently no events planned',
                        title='No events upcoming')
        
        for r in res:
            obj = r.getObject()
            link = "%s/@@hw.telescope?path=%s" % (self.getEventsfolderUrl(), r.getPath())
            description = obj.Description().strip() != '' and obj.Description() or obj.getText()
            yield dict(link=link, location=r.location, start=obj.start(), description=description,
                title=obj.Title())

    def getEventsDict(self, limit=0):
        """ preps the events ordered by month """
        events = self.getEvents(limit)
        now = DateTime()

        edict = {}
        ordereddates = []

        if events:
            for event in events:
                ## if event['end']<now: continue
                date = DateTime(event['start'].Date())
                date = DateTime("%s-%s-01" % (date.year(), date.mm()))
                if date not in ordereddates:
                    ordereddates.append(date)
                edict[date] = edict.get(date, []) + [event]

        return edict, ordereddates


    def getPublications(self, limit=0):
        """ Fetch campaign-relevant publications """
        subject = aq_inner(self.root).Subject()
        pc = getToolByName(self.context, 'portal_catalog')
        res = pc(object_provides='slc.publications.interfaces.IPublicationEnhanced', 
            portal_type='File',
            Subject=subject,
            Language=['en',''],
            sort_on="effective", sort_order="reverse")
        if len(res) and limit > 0:
            res = res[:limit]
        for r in res:
            obj = r.getObject()
            # now get the correct translation, or use the EN one as fallback
            obj = obj.getTranslation(self.pref_lang) or obj
            link = '/'.join(obj.getPhysicalPath()).replace('/osha/portal', 'https://osha.europa.eu')
            url = obj.absolute_url()
            yield dict(url=url, link=link, title=obj.Title(), description=obj.Description(),
                obj=obj)

    def getPromo(self):
        """ Get the promotional doc """
        promo = getattr(aq_inner(self.langroot), 'promo', None)
        return promo

    def getOCPLogos(self):
        """ fetch the partner logos, the folder path is hardcoded """
        path = 'en/about/campaign-partners/img'
        folder = self.root.restrictedTraverse(path)
        partners_folder = aq_parent(folder)
        images = folder.objectItems('ATImage')
        for id, image in images:
            if '.' in id:
                elems = id.split('.')
                stem = '.'.join(elems[0:-1])
            else:
                stem = id
            if stem.split('_')[-1] == 'logo':
                yield dict(src=image.absolute_url(),
                link="%s/detail?id=%s" % (partners_folder.absolute_url(), stem.replace('_logo', '')))

    def getNapofilmId(self):
        """ Looks for a property called napofilm on the subsite root"""
        id = self.root.getProperty('napofilm', '')
        return id

    def getImageFolders(self):
        """Get all image folders tagged with the campaign subject"""
        multimedia_path = "/osha/portal/en/press/photos"
        subject = aq_inner(self.root).Subject()
        pc = getToolByName(self.context, 'portal_catalog')
        res = pc(portal_type='Folder', Subject=subject, path=multimedia_path)
        #import pdb; pdb.set_trace()
        image_folders = dict()
        max_images_per_folder = 10
        for r in res:
            folder = r.getObject()
            images = dict()
            image_count = 0
            for image in folder.listFolderContents():
                if image_count >= max_images_per_folder:
                    break
                if image.portal_type == "Image":
                    images[image.id] = {"title" : image.title}
                    image_count += 1
            if images:
                yield dict(title=folder.Title(),
                    images=images,
                    folder_url='/'.join(folder.getPhysicalPath()).replace('/osha/portal', 'https://osha.europa.eu'),
                    )

    def recreate_language_links(self):
        """ ZopeFinds through the en tree and links languages """
        assert (self.context.getId()=='hw2012')
        langs = self.context.portal_languages.getSupportedLanguages()
        canonical = self.context['en']
        for lang in langs:
            if lang == 'en': 
                continue
            if lang in self.context.objectIds():
                langfolder = self.context[lang]
                langfolder.setLanguage('')
                langfolder.setLanguage(lang)
                langfolder.addTranslationReference(canonical)

        LT = canonical.restrictedTraverse('@@linguatools-old')
        LT.fixTranslationReference(recursive=True)
        return "done"

    def copy_seo_description(self):
        """ copys any text found in the description into seo description, if not present """
        assert (self.context.getId()=='hw2012')
        msg = ''
        can = self.context.en
        for id, item in can.ZopeFind(can, search_sub=1):
            if item.meta_type=="Script (Python)": continue
            if not hasattr(item.aq_explicit, "Schema"):
                continue
            if not 'seoDescription' in item.Schema().keys():
                continue

            for lang in item.getTranslations():
                trans = item.getTranslation(lang)
                desc = trans.Description()
                seodesc = trans.getField('seoDescription').getAccessor(trans)().strip()
                if not seodesc and desc:
                    trans.getField('seoDescription').getMutator(trans)(desc)
                    msg += "Set seo desc for %s:%s\n" % (lang, id)
                
        return msg
        
        
    def set_views(self):
        """ sets the views on all folders """
        # make sure we are called on the campaign root folder
        assert (self.context.getId()=='hw2012')
        msg = "HW Helper - set_views\n====================\n\n"
        for lang in self.supported_langs:
            msg += "LANGUAGE: %s\n============\n\n" % lang.upper()

            if lang not in self.context.objectIds():
                continue

            langfolder = self.context[lang]
            
            for path in SV:
                ob = langfolder.restrictedTraverse(path, None)
                if ob is None:
                    msg += "ERROR, %s/%s not found\n" % (lang, path)
                    continue
                msg += self._sp(ob, 'layout', SV[path])

        self.context.REQUEST.RESPONSE.setHeader('Content-type', 'text/plain')
        return msg


    def _sp(self, ob, id, value, type="string"):
        """ simple set property. Checks if present """
        msg = ""
        # XX = ob.getProperty(id, '')
        # if XX.startswith('hw2012_'):
        #     msg += "Skipping %s, preserving already set\n" % ob.absolute_url(1)
        #     return msg
        if ob.meta_type=='Script (Python)' or not hasattr(ob.aq_explicit, 'portal_type') or ob.portal_type not in ('Folder', 'Document', 'Topic'):
            msg+= "xx not a content object, skipping.."
            return msg    
        if not ob.hasProperty(id):
            try:
                ob._setProperty(id, value, type)
            except:
                import pdb; pdb.set_trace()
            msg+=".. set new layout property: %s\n" % ob.absolute_url(1)
        else:
            ob._updateProperty(id, value)
            msg+=".. update layout property: %s\n" % ob.absolute_url(1)
        return msg

    def cls_by_str(self, text):
        """ calculate text size indicator for styling. Used in the navigation """
        if len(text)<=22:
            return None
        elif 22<len(text)<50:
            return 'char-20'
        else:
            return 'char-50'

    def len_month(self, month=1):
        """ calculate class and month name based on number """
        ts = self.context.translation_service

        tmon = ts.utranslate(domain='plonelocales', msgid=ts.month_msgid(month), context=self.context)
        ltmon = len(tmon)

        return (tmon, ltmon)
