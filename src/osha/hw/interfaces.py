from zope.interface import Interface

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

    def getEventsfolderUrl():
        """ URL to the events-folder"""

    def getHomeURL():
        """ Campaing site root URL """

    def getPromo():
        """ Get the promotional doc """

class INationalPartnerForm(Interface):
    """ """

    def get_validation_messages(self):
        """ """ 

