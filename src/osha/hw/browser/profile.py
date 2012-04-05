from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from osha.hw.browser.sync_receiver import BaseDBView
from osha.hw.queries import *


class _OrgOverview(BaseDBView):

    def get_partners(self):
        res = self.conn.execute(self.get_org_q)
        return res

    def get_partners_atoz(self):
        partners = self.conn.execute(self.get_org_q)
        atoz = dict()
        for partner in partners:
            initial = partner["title"][0].upper()
            if initial in atoz:
                atoz[initial].append(partner)
            else:
                atoz[initial] = [partner]
        return atoz


class OCPsOverview(_OrgOverview):

    get_org_q = get_ocps


class FOPsOverview(_OrgOverview):

    get_org_q = get_fops


class _OrgDetail(BaseDBView):

    def get_partner(self, id=''):
        partner = self.conn.execute(self.get_org_by_id_q % dict(id=id))
        return partner.fetchone()

    def get_partner_events(self, partner_id=''):
        events = self.conn.execute(self.get_org_events_q % \
        dict(partner_id=partner_id))
        return events

    def get_partner_news(self, partner_id=''):
        events = self.conn.execute(self.get_org_news_q % \
        dict(partner_id=partner_id))
        return events


class OCPDetail(_OrgDetail):

    get_org_by_id_q = get_ocp_by_id
    get_org_events_q = get_ocp_events
    get_org_news_q = get_ocp_news


class FOPDetail(_OrgDetail):

    get_org_by_id_q = get_fop_by_id
    get_org_events_q = get_fop_events
    get_org_news_q = get_fop_news
