import logging
import simplejson as json

from zope.interface import implements
from zope.i18n import translate

from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Archetypes import PloneMessageFactory as _

from osha.hw.interfaces import INationalPartnerForm

log = logging.getLogger('osha.hw2012.browser.forms')

class NationalPartnerForm(BrowserView):
    """ """
    implements(INationalPartnerForm)

    def get_validation_messages(self):
        """ """
        context = aq_inner(self.context)
        request = context.REQUEST
        fieldnames = {
            'organisation': translate(_('Company/Organisation')),
            'address': translate(_('Address')),
            'postal_code': translate(_('Postal Code')),
            'city': translate(_('City')),
            'country': translate(_('Country')),
            'firstname': translate(_('Firstname')),
            'lastname': translate(_('Lastname')),
            'sector': translate(_('Sector')),
            'email': translate(_('Email')),
            'telephone': translate(_('Telephone')),
            }
        lang = context.portal_languages.getPreferredLanguage()
        messages = {}

        for field_id in fieldnames:
            fieldname = fieldnames[field_id]
            err_msgs = {
                'required': translate(
                            _(u'error_required',
                            default=u'${name} is required, please correct.',
                            mapping={'name': fieldname}),
                            context=request,
                            ),

                'email': translate(
                            _(u"You entered an invalid email address."),
                            context=request,
                            ),
                }

            messages[field_id] = err_msgs

        data = {'messages': messages}
        return json.dumps(data)
