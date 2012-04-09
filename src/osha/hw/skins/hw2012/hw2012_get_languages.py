# Copied from plone.app.i18n.locales.browser.selector.LanguageSelector [thomasw]

plt = context.portal_languages

bound = plt.getLanguageBindings()
current = bound[0]

def merge(lang, info):
    info["code"]=lang
    if lang == current:
        info['selected'] = True
    else:
        info['selected'] = False
    return info

languages = [merge(lang, info) for (lang,info) in
                plt.getAvailableLanguageInformation().items()
                if info["selected"]]


languages.sort(lambda x,y: cmp(x['native'], y['native']))

return languages
