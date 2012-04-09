portal = context.portal_url.getPortalObject()
canonical = portal.en.press
contactInfo = list()
folder = getattr(canonical, 'press-contacts')
international = getattr(folder, 'international-press', None)
if international:
    contactInfo.append(international)
spanish = getattr(folder, 'spanish-press', None)
if spanish:
    contactInfo.append(spanish)
brussels = getattr(folder, 'brussels-liaison', None)
if brussels:
    contactInfo.append(brussels)

return contactInfo
