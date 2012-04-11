from Acquisition import aq_inner
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

from logging import getLogger
log = getLogger('osha.hw helper')

IEXT = ('gif', 'jpg', 'png')
TOPLEVELFOLDERS = ('about', 'get-involved', 'leadership', 'media', 'resources', 'worker-participation')
SV = {
    'leadership': 'hw2012_landing_page',
    'leadership/leadership': 'hw2012_landing_page',
    'leadership/benefits/index_html': 'hw2012_details_page',
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
    'about/campaign-partners/index_html': 'hw_ocps',
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

# consider translating the strings
email_template = """<p>Thank you for signing the European Week Charter.</p>

<p>Please find a PDF version of the charter attached to this email, which you may print.</p>

<p>For more information on the Healthy Workplaces Campaign, please consult the website at http://www.healthy-workplaces.eu.</p>


"""


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

class CharterView(BaseDBView):

    def __call__(self):

        request = self.context.REQUEST
        language = self.context.portal_languages.getPreferredLanguage()

        portal = self.context.portal_url.getPortalObject()
        url = "/%s/get-involved/" % language

        organisation    = request.get('organisation', '')
        address         = request.get('address', '')
        postal_code     = request.get('portal_code', '')
        city            = request.get('city', '')
        country         = request.get('country', '')
        firstname       = request.get('firstname', '')
        lastname        = request.get('lastname', '')
        sector          = request.get('sector', '')
        email           = request.get('email', '')
        telephone       = request.get('telephone', '')
        checkboxlist    = request.get('checkboxlist', [])
        other           = request.get('other_activities_text', '')

        checkboxes = {}
        for c in checkboxlist:
            args = c.split('_', 1)
            if args[1]=='other':
                args[1] = other
            checkboxes[int(args[0])] = args[1]

        cb_list = ['0' for x in range(10)]
        for k in checkboxes.keys():
            cb_list[k] = '1'

        checkboxint=''.join(cb_list)

        if 1:
            now = DateTime().ISO()  
            
            query = insert_hw2012_charter % dict( 
                        Organisation    = organisation,
                        Address         = address, 
                        Postalcode      = postal_code,
                        City            = city,
                        Country         = country,
                        Firstname       = firstname,
                        Lastname        = lastname,
                        Function        = sector,
                        Email           = email,
                        Telephone       = telephone,
                        Commitment      = checkboxint,
                        Commitment_other = other,
                        Date            = now,
                        Sector          = sector,
                        Language  = language
                        )
            self.conn.execute(query)
            
        from_address = 'information@osha.europa.eu'

        try:
            logit (" ... calling generatePDF, language: %s" % language)
            logit (" ... calling generatePDF")
            pdf = generatePDF(self.context,
                                company=organisation, 
                                language=language, 
                                firstname=firstname, 
                                lastname=lastname, 
                                checkboxes=checkboxes, 
                                usePDFTK=0 
                                )

            logit (" ... generatePDF called!")
            send_charter_email(self.context, pdf=pdf, to=email, sender=from_address, body=email_template, language=language)

        except Exception, e: #XXX Too many things could possibly go wrong. So we catch all.
            exception = self.context.plone_utils.exceptionString()
            logit("Exception: " + exception)
            raise
            return request.RESPONSE.redirect(url+'?portal_status_message='+str(e)) # context.set(status='failure', portal_status_message='Error: '+exception)

        request.RESPONSE.redirect(url)

    def create_table(self):
        """ create the table """
        self.conn.execute(create_hw2012_charter)
        return "Table created"
    

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
        return "http://hw2012.syslab.com"

    def getNewsfolderUrl(self):
        return self.langroot.restrictedTraverse('news').absolute_url()

    def getEventsfolderUrl(self):
        return self.langroot.restrictedTraverse('events').absolute_url()

    def getNews(self, limit=None):
        """Fetch campaign-related News and return the relevant parts"""
        subject = aq_inner(self.root).Subject()
        portal_path = self.ptool.getPortalPath()
        pc = getToolByName(self.context, 'portal_catalog')
        res = pc(portal_type='News Item', sort_on='effective',
            sort_order='reverse',
            expires={'query': DateTime(), 'range': 'min'},
            path=['%s/en' % portal_path, '%s/%s' % (portal_path, self.pref_lang),
            self.subsite_path],
            Subject=subject)[:limit]
        for r in res:
            obj = r.getObject()
            link = "%s/@@slc.telescope?path=%s" % (self.getNewsfolderUrl(), r.getPath())
            img_url = getattr(obj, 'image', None) and obj.image.absolute_url() or ''
            description = obj.Description().strip() != '' and obj.Description() or obj.getText()
            yield dict(link=link, img_url=img_url, description=description,
                title=obj.Title())

    def getEvents(self, limit=None):
        """Fetch campaign-related Events and return the relevant parts"""
        subject = aq_inner(self.root).Subject()
        portal_path = self.ptool.getPortalPath()
        pc = getToolByName(self.context, 'portal_catalog')
        res = pc(portal_type='Event', sort_on='effective',
            sort_order='reverse',
            end={'query': DateTime(), 'range': 'min'}, expires={'query': DateTime(), 'range': 'min'},
            path=['%s/en' % portal_path, '%s/%s' % (portal_path, self.pref_lang),
            self.subsite_path],
            Subject=subject)[:limit]
        for r in res:
            obj = r.getObject()
            link = "%s/@@slc.telescope?path=%s" % (self.getEventsfolderUrl(), r.getPath())
            description = obj.Description().strip() != '' and obj.Description() or obj.getText()
            yield dict(link=link, location=r.location, start=obj.start(), description=description,
                title=obj.Title())

    def fixcontent(self):
        """ due to the url change, we have broken links in the translations """

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
            
            for path in SV:
                ob = langfolder.restrictedTraverse(path, None)
                if ob is None:
                    msg += "ERROR, %s/%s not found\n" % (lang, path)
                    continue
                msg += self._sp(ob, 'layout', SV[path])

        self.request.RESPONSE.setHeader('Content-type', 'text/plain')
        return msg


    def _sp(self, ob, id, value, type="string"):
        """ simple set property. Checks if present """
        msg = ""
        # XX = ob.getProperty(id, '')
        # if XX.startswith('hw2012_'):
        #     msg += "Skipping %s, preserving already set\n" % ob.absolute_url(1)
        #     return msg
            
        if not ob.hasProperty(id):
            ob._setProperty(id, value, type)
            msg+=".. set new layout property: %s\n" % ob.absolute_url(1)
        else:
            ob._updateProperty(id, value)
            msg+=".. update layout property: %s\n" % ob.absolute_url(1)
        return msg


