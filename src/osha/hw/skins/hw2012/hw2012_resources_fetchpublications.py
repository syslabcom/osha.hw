# in ticket 1311 manuela/heike request to remove the special treatment for the first three publications. Changed on 11/06/2010

lang = context.portal_languages.getPreferredLanguage()

publication_paths = [
  '/%s/publications/e-facts/48.pdf' %lang,
  '/%s/publications/factsheets/%s_89.pdf' %(lang, lang), 
  '/%s/publications/factsheets/%s_88.pdf' %(lang, lang)
]

highlighted_publications = []

#for path in publication_paths: 
#  pub = context.restrictedTraverse('/osha/portal'+path, None)
#  if pub is not None:
#    highlighted_publications.append(pub)

maintenance_publications = []

# Fetch the EN version, needed for language fallback *sigh*
morepubs = context.portal_catalog(object_provides='slc.publications.interfaces.IPublicationEnhanced', 
    portal_type='File',
    Subject=['management_leadership', 'worker_participation'],
    Language=['en',''],
    sort_on="effective", sort_order="reverse")
for pub in morepubs:
  ob = pub.getObject()
  # now get the correct translation, or use the EN one as fallback
  ob = ob.getTranslation(lang) or ob
  #if ob not in highlighted_publications:
  maintenance_publications.append(ob)

#return [highlighted_publications, maintenance_publications]
return [[], maintenance_publications]
