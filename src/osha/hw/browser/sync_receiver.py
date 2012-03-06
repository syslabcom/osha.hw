from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from collective.lead.interfaces import IDatabase
from Products.Five import BrowserView
from zope.component import getUtility
import sqlalchemy
from osha.hw.queries import create_statements


class BaseDBView(BrowserView):

    def __init__(self, context, request, **kw):
        self.context = context
        self.db = getUtility(IDatabase, name="osha.database")
        self.conn = self.db.connection

class DBSetup(BaseDBView):

    def __call__(self):
        for query in create_statements:
            self.conn.execute(query)

class AddOCP(BaseDBView):
    
    def __call__(self, partners):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        pwt = portal.portal_workflow
        #targetfolder = getattr(context, 'eu-partners-folder')
        targetfolder = self.context


        
        fieldnames, p_data = partners
        values = dict()
        for i in range(len(fieldnames)):
            val = p_data[i]
            if val == '':
                val = None
            values[fieldnames[i]] = val

#        if bool(portal.scripts.hw2010_is_partner_available(id=values['id'])[0]['count']):
#          try:
#            ret = portal.scripts.hw2010_update_partner_data(values)
#          except Exception, err:
#            return str(err)
#        else:
#          portal.scripts.hw2010_insert_partner_data(values)

        print values

        return 0
