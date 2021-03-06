from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IHWThemeLayer(IDefaultPloneLayer):
    """ Marker Interface used by BrowserLayer
    """

class IAddOCP(Interface):
    """ Add an Official Campaign Partner """


class IAddFOP(Interface):
    """ Add a Focal Point """


class IAddImage(Interface):
    """ Add an image to a partner or FOP"""


class IAddEvent(Interface):
    """ Add an event and link it to a profile"""


class IAddNews(Interface):
    """ Add a news item and link it to a profile """

class IHelperView(Interface):
    """ """
    
    def set_views():
        """ sets the views on all folders """

    def recreate_language_links():
        """ ZopeFinds through the en tree and links languages """

    def getTranslations():
        """ return translations of current item """

    def getNavigation():
        """ Fetch landing and sub-pages """

    def getNews(limit=None):
        """ Fetches campaign-related news """

    def getNewsfolderUrl():
        """ URL to the news-folder"""

    def getEvents(limit=None):
        """ Fetches campaign-related events """

    def getPublications(limit=None):
        """ Fetch campaign-relevant publications """

    def getEventsfolderUrl():
        """ URL to the events-folder"""

    def getHomeURL():
        """ Campaing site root URL """

    def getPromo():
        """ Get the promotional doc """

    def getOCPLogos():
        """ fetch the partner logos, the folder path is hardcoded """

    def getSlogan():
        """ Fetches the translated slogan text """

    def getNapofilmId():
        """ Looks for a property called napofilm on the subsite root"""

    def len_month(month=1):
        """ calculate class and month name based on number """

    def getEventsDict(limit=0):
        """ preps the events ordered by month """

    def copy_seo_description():
        """ copys any text found in the description into seo description, if not present """

    def getImageFolders():
        """Get all image folders tagged with the campaign subject"""

    def cls_by_str(text):
        """ calculate text size indicator for styling. Used in the navigation """


class INationalPartnerForm(Interface):
    """ """

    def get_validation_messages(self):
        """ """ 

