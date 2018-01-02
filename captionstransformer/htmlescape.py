try:
    from htmlentitydefs import codepoint2name
except ImportError:
    from html.entities import codepoint2name

def htmlescape(text):    
    d = dict((unichr(code), u'&%s;' % name) for code,name in codepoint2name.iteritems() if code!=38) # exclude "&"    
    if u"&" in text:
        text = text.replace(u"&", u"&amp;")
    for key, value in d.iteritems():
        if key in text:
            text = text.replace(key, value)
    return text