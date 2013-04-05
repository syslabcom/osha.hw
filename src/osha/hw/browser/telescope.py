import logging

from ordereddict import OrderedDict
from Acquisition import aq_base, aq_inner, aq_acquire

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.publisher.interfaces import NotFound
from zope.component import getMultiAdapter

logger = logging.getLogger('osha.theme/browser/telescope.py')

class TelescopeView(BrowserView):
    """
    Renders an object in a different location of the site when passed the
    path to it #1150
    """

    def __call__(self, *args, **kw):
        """
        Uses ac_aqcuire to return the specified page template
        """
        if self.request.has_key("path"):
            path = self.request["path"]
            target_obj = None
            try:
                target_obj = self.context.restrictedTraverse(path)
            except KeyError:
                logger.log(logging.INFO, "Invalid path: %s" %path)
                raise NotFound
            if target_obj:
                context = self.context
                request = self.request
                view = ""
                try:
                    # Strip the target_obj of context with aq_base.
                    # Put the target in the context of self.context.
                    # getDefaultLayout returns the name of the default
                    # view method from the factory type information
                    view = aq_acquire(aq_base(target_obj).__of__(context),
                                       target_obj.getDefaultLayout())(**kw)

                except AttributeError, message:
                    logger.log(logging.ERROR,
                               "Error acquiring template: %s, path: %s"\
                               %(message, path))
                    raise NotFound
                if view:
                    # All images and links in the target document
                    # which depend on the context e.g. images in News
                    # items, will be broken, so we do a simple replace
                    # to fix them.

                    # I tried to be a bit more clever about this and
                    # use the lxml soupparser, but it breaks the
                    # layout severely when it is converted back to
                    # html (deroiste)
                    proxy_url = context.absolute_url() + "/" +\
                                 target_obj.getId()
                    target_url = '/'.join(target_obj.getPhysicalPath()).replace('/osha/portal', 'https://osha.europa.eu')
                    if target_obj.portal_type == 'News Item':
                        txt = '''<p id="more"><a href="../news" class="more"><span i18n:translate="label_more_news" tal:omit-tag="">More news</span>&hellip;</a>\n<h1 class="documentFirstHeading">'''
                        view = view.replace('<h1 class="documentFirstHeading">', txt)
                    elif target_obj.portal_type == 'Event':
                        txt = '''<p id="more"><a href="../events" class="more"><span i18n:translate="label_more_events" tal:omit-tag="">More events</span>&hellip;</a>\n<h1 class="documentFirstHeading">'''
                        view = view.replace('<h1 class="documentFirstHeading">', txt)
                    return view.replace(proxy_url, target_url)

        else:
            logger.log(logging.INFO, "No path specified")
            raise NotFound

    def telescope_translations(self):
        """Return the titles and URLs of translations, include the
        relevant telescope path if accessed via @@hw.telescope
        #6509"""
        context = self.context
        request = context.REQUEST

        actual_url = request.ACTUAL_URL
        is_telescope = "hw.telescope" in actual_url
        if is_telescope:
            parent = request.PARENTS[0]
            query_string = request.QUERY_STRING

        translations = context.getTranslations()
        lang_codes = sorted(translations.keys())

        lang_tool = getToolByName(context, "portal_languages")
        lang_info = lang_tool.getAvailableLanguageInformation()

        transdict = OrderedDict()
        for lang_code in lang_codes:
            translation = translations[lang_code][0]
            if is_telescope:
                trans_parent = parent.getTranslation(lang_code)
                # The target URL may exist even if there is no such
                # translation for the telescope origin
                if trans_parent:
                    parent_url = "{0}/@@hw.telescope".format(
                        trans_parent.absolute_url())
                else:
                    parent_url = actual_url
                url = "{0}?path={1}".format(
                        parent_url, translation.absolute_url_path())
            else:
                url = translation.absolute_url()

            is_hw_root = context.getPhysicalPath()[-1] == 'hw2012'
            quote = is_hw_root and translation.getText() or ''

            transdict[lang_code] = {
                'url': url,
                'title': lang_info[lang_code]["native"],
                'quote': quote,
                'css_class': translation = context and 'current' or  ''
                }
        return transdict
