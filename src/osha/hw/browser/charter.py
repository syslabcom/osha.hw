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

from logging import getLogger
log = getLogger('osha.hw helper')




# consider translating the strings
email_template = """<p>Thank you for signing the European Week Charter.</p>

<p>Please find a PDF version of the charter attached to this email, which you may print.</p>

<p>For more information on the Healthy Workplaces Campaign, please consult the website at http://www.healthy-workplaces.eu.</p>


"""

class CharterView(BaseDBView):

    def __call__(self):

        request = self.context.REQUEST
        language = self.context.portal_languages.getPreferredLanguage()

        portal = self.context.portal_url.getPortalObject()
        url = "/%s/get-involved/become-a-national-partner/feedback" % language

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
            try:
                self.conn.execute(query)
            except Exception, e:
                raise e

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
            #self.context.REQUEST.RESPONSE.setHeader('Content-type', 'application/pdf')
            #return pdf
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
