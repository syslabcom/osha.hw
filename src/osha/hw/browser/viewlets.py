from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from osha.theme.browser.viewlets import OSHAFooterActions

unwanted_actions = ['sendto', 'sitemap', 'osha_update', 'osha_translations']


class HWFooterActions(OSHAFooterActions):

    _template = ViewPageTemplateFile('templates/footer_actions.pt')

    def update(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')

        self.portal = portal_state.portal()
        self.site_url = portal_state.portal_url()

        self.portal_actionicons = aq_base(getToolByName(self.context,
            'portal_actionicons'))

        document_actions = context_state.actions().get('document_actions',
            None)
        footer_actions = context_state.actions().get('footer_actions', None)
        site_actions = context_state.actions().get('site_actions', None)
        actions = document_actions + footer_actions + site_actions
        actions = [x for x in actions if x['id'] not in unwanted_actions]
        self.hw_actions = list()
        for action in actions:
            action['url'] = '%s' % action['url'].replace(self.site_url, \
            'https://osha.europa.eu')
            self.hw_actions.append(action)

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor
