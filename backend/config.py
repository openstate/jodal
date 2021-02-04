import os

# On a new deployment (whether production or development) make
# a copy of this file called 'config.py' and change 'False' for
# SECRET_KEY to a newly generated string using these python commands:
# $ import os
# $ os.urandom(24)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'DitIsJodal'
    NAME_OF_APP = 'jodal'
#    SERVER_NAME = 'waarismijnstemlokaal.nl'
#    PREFERRED_URL_SCHEME = 'https'
#    FORCE_HOST_FOR_REDIRECTS = 'waarismijnstemlokaal.nl'
#    USE_SESSION_FOR_NEXT = True
    # authfusion config stuff
    CLIENT_ID="47067915-8bfd-4e57-957c-a232e2025524"
    CLIENT_SECRET="QyT2uwYGHx5jp4FKY9EmYcsBWhP7s0lXupncdoo3SP8"
    FA_URL='http://localhost:9011'
    AUTHORIZATION_BASE_URL='http://localhost:9011/oauth2/authorize'
    TOKEN_URL='http://fusionauth:9011/oauth2/token'
    USERINFO_URL='http://fusionauth:9011/oauth2/userinfo'
    REDIRECT_URI='http://api.jodal.nl/users/simple/callback'
    API_KEY='tmrbxxsqGVgbXEZvYpETKb2gzr-7WWPni8jL-3MiotfAULKUH7nhax3m'
    FORM_ID='c53c5260-6580-4ab3-80d8-b6d4c4042570'
