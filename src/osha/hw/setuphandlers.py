import os
import logging
import transaction
from zope.app.component.hooks import getSite
from zope.component import getUtility

def importVarious(context):
    if context.readDataFile("osha-hw-various.txt") is None:
        return
