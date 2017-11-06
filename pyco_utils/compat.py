import sys
import six

# Useful for very coarse version differentiation.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)
# 判断py2 还是 py3

if PY3:
    from urllib.parse import quote_plus
    from urllib.request import urlopen
    from base64 import decodebytes, encodebytes


    def u(s):
        return s


    def b(s):
        return s.encode("utf-8")
else:
    from urllib import quote_plus
    from urllib2 import urlopen
    from base64 import decodestring as decodebytes
    from base64 import encodestring as encodebytes


    def u(s):
        return unicode(s.replace(r'\\', r'\\\\'), "unicode_escape")


    def b(s):
        return s
