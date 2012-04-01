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
