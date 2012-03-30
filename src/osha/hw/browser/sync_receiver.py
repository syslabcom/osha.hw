from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from collective.lead.interfaces import IDatabase
from Products.Five import BrowserView
from zope.component import getUtility
import sqlalchemy
from osha.hw.queries import *


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
        targetfolder = self.context

        fieldnames, p_data = partners
        values = dict(zip(fieldnames, p_data))
        if self.conn.scalar(is_ocp_available % values) > 0:
            self.conn.execute(update_ocp % values)
        else:
            self.conn.execute(insert_ocp % values)

        print values
        return 0


class AddFOP(BaseDBView):

    def __call__(self, partners):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        pwt = portal.portal_workflow
        targetfolder = self.context

        fieldnames, p_data = partners
        values = dict(zip(fieldnames, p_data))
        if self.conn.scalar(is_fop_available % values) > 0:
            self.conn.execute(update_fop % values)
        else:
            self.conn.execute(insert_fop % values)

        print values
        return 0


class AddImage(BaseDBView):

    def __call__(self, id, image, path):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        targetfolder = portal.restrictedTraverse(path)
        if not getattr(targetfolder, id, None):
            targetfolder.invokeFactory(id=id, type_name=u"Image")

        ob = getattr(targetfolder, id)
        ob.setImage(image.data)

        return 0
