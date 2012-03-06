from Products.CMFCore.utils import getToolByName
from collective.lead.interfaces import IDatabase
from Products.Five import BrowserView
from zope.component import getUtility
import sqlalchemy
from osha.hw.queries import create_statements


class BaseDBView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.db = getUtility(IDatabase, name="osha.database")
        self.conn = self.db.connection

class DBSetup(BaseDBView):

    def __call__(self):
        for query in create_statements:
            self.conn.execute(query)

class AddOCP(BaseDBView):
    
    def __call__(self):
        print "HALLOO"