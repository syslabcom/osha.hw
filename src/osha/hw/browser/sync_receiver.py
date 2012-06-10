import Acquisition
from OFS.Image import File
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from osha.policy.interfaces import IDatabaseSettings
from Products.Five import BrowserView
from zope.component import getUtility
import sqlalchemy
from osha.hw.queries import *
from slc.subsite.root import getSubsiteRoot

from logging import getLogger
log = getLogger('osha.hw sync-receiver')


class BaseDBView(BrowserView):

    def __init__(self, context, request, **kw):
        self.context = context
        self.db = getUtility(IDatabaseSettings)
        self.conn = self.db.connection
        self.subsite_path = getSubsiteRoot(Acquisition.aq_inner(context))
        self.root = self.context.restrictedTraverse(self.subsite_path)

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


class AddEvent(BaseDBView):

    def __call__(self, partner_id, partner_type, id, title, description,
    text, start, end, location, attendees, eventurl, contactname, contactemail,
    contactphone, dateToBeConfirmed, attachment_data, attachment_name):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        pwt = getToolByName(portal, 'portal_workflow')

        targetfolder = self.context
        if id not in targetfolder.objectIds():
            targetfolder.invokeFactory(id=id, type_name=u"Event")

        ob = getattr(targetfolder, id, None)
        if ob is None:
            return "Error, object not found"

        ob.setTitle(title)
        # all events language neutral I assume
        ob.setLanguage('')
        ob.setDescription(description)
        ob.setText(text)
        ob.setStartDate(start)
        ob.setEndDate(end)
        ob.setLocation(location)
        ob.setAttendees(attendees)
        ob.setEventUrl(eventurl)
        ob.setContactName(contactname)
        ob.setContactEmail(contactemail)
        ob.setContactPhone(contactphone)
        tbc = ob.getField('dateToBeConfirmed')
        if tbc:
            tbc.getMutator(ob)(dateToBeConfirmed)

        # set the subcategory
        ob.setSubcategory(self.root.Subject())
        #import pdb; pdb.set_trace()

        # Set attachment
        if len(attachment_data.data) > 0:
            mutator = ob.getField('attachment').getMutator(ob)
            fileob = File(attachment_name, attachment_name,
                attachment_data.data)
            setattr(fileob, 'filename', attachment_name)
            mutator(fileob)

        # publish
        try:
            pwt.doActionFor(ob, 'publish')
        except:
            pass

        ob.reindexObject()
        log.info('Created new event at %s' % ob.absolute_url())

        if partner_id:
            if partner_type == 'OCP':
                checker = is_ocp_event_available
                updater = update_ocp_event
                inserter = insert_ocp_event
            elif partner_type == 'FOP':
                checker = is_fop_event_available
                updater = update_fop_event
                inserter = insert_fop_event

            if self.conn.scalar(checker % \
            dict(partner_id=partner_id, id=id)) > 0:
                self.conn.execute(updater % dict(partner_id=partner_id, id=id,
                    url='/'.join(ob.getPhysicalPath())))
            else:
                self.conn.execute(inserter % dict(partner_id=partner_id,
                    id=id, url='/'.join(ob.getPhysicalPath())))

        return 0


class AddNews(BaseDBView):

    def __call__(self, partner_id, partner_type, id, title, description, text,
    effective, image):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        pwt = portal.portal_workflow
        targetfolder = self.context

        if not getattr(targetfolder, id, None):
            targetfolder.invokeFactory(id=id, type_name=u"News Item")

        ob = getattr(targetfolder, id, None)
        if ob is None:
            return "Error, object not found"

        # if there's only content in text, but none in description:
        if text != '' and description == '':
            description = text
            text = ''

        ob.setTitle(title)
        # all news items are language neutral I assume
        ob.setLanguage('')
        ob.setDescription(description)
        ob.setText(text)
        ob.setEffectiveDate(DateTime(effective))

        ob.setImage(image.data)

        # #set Subject
        ob.setSubject(self.root.Subject())

        # publish
        try:
            pwt.doActionFor(ob, 'publish')
        except:
            pass

        log.info('Transferred item with Title "%s" to URL: %s' % \
        (title, ob.absolute_url()))

        ob.reindexObject()

        if partner_id:
            if partner_type == 'OCP':
                checker = is_ocp_news_available
                updater = update_ocp_news
                inserter = insert_ocp_news
            elif partner_type == 'FOP':
                checker = is_fop_news_available
                updater = update_fop_news
                inserter = insert_fop_news

            if self.conn.scalar(checker % \
            dict(partner_id=partner_id, id=id)) > 0:
                self.conn.execute(updater % dict(partner_id=partner_id, id=id,
                    url='/'.join(ob.getPhysicalPath())))
            else:
                self.conn.execute(inserter % dict(partner_id=partner_id,
                    id=id, url='/'.join(ob.getPhysicalPath())))
        return 0
