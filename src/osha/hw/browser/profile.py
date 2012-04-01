from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from osha.hw.browser.sync_receiver import BaseDBView
from osha.hw.queries import *


class OCPsOverview(BaseDBView):
    
    def get_partners(self):
        res = self.conn.execute(get_ocps)
        return res
    
    def get_partners_atoz(self):
        partners = self.conn.execute(get_ocps)
        atoz = dict()
        for partner in partners:
            initial = partner["title"][0].upper()
            if initial in atoz:
                atoz[initial].append(partner)
            else:
                atoz[initial] = [partner]
                
        return atoz
