#! /usr/bin/env python3

hostname = 'icloud.com'
isSSL = True
server = 'ilocal.dd'
port = 443
domain = server if port in [443,80] else '{}:{}'.format(server,port)


inject_domain = [
    ['icloud.developer.apple.com', 'icloud.developer.'+domain],
    ['icloud.com.cn', 'cn.'+domain],
    ['iCloud.com.cn', 'cn.'+domain],
    ['cdn.apple-cloudkit.com', 'cdncloud.'+domain],
    ['setup.icloud.com', 'setup.'+domain],
    ['appleid.cdn-apple.com', 'appleidcdn.'+domain],
    ['idmsa.apple.com.cn', 'cnidmsa.'+domain],
    ['idmsa.apple.com', 'idmsa.'+domain],
    ['feedbackws.apple-cloudkit.com', 'feedbackws-cloudkit.'+domain],
    ['feedbackws.icloud.com', 'feedbackws.'+domain],
    ['www.apple.com', 'wwwapple.'+domain],
    ['appleid.apple.com', 'appleid.'+domain],
    ['id.apple.com', 'id.'+domain],
    ['api.apple-cloudkit.com', 'apicloudkit.'+domain],
    ['support.apple.com', 'support.'+domain],
    ['iforgot.apple.com', 'iforgot.'+domain],
    ['signin.apple.com', 'signin.'+domain],
    ['gsa.apple.com', 'gsa.'+domain],
    ['icloud.com', domain],
    ['iCloud.com', domain],
    ['apple.com', 'apple.'+domain],
]

req_headers = [
    ['', {'Host':'www.icloud.com', 'Accept-Encoding':'gzip, deflate', 'Connection':'close'}],
    ['appleauth/auth', {'Host':'idmsa.apple.com', }],
    ['jslog', {'Host':'idmsa.apple.com',}],
    ['reportRaw', {'Host':'feedbackws.icloud.com'}],
    ['reportStats', {'Host':'feedbackws.icloud.com'}],
    ['setup/ws/1/', {'Host':'setup.icloud.com'}],
    ['/authService.latest.min.js', {'Host':'appleid.cdn-apple.com'}],
    ['appleauth/static', {'Host':'appleid.cdn-apple.com'}],
    ['ck/2', {'Host':'cdn.apple-cloudkit.com'}],
    ['/ac/', {'Host':'www.apple.com'}],
    ['wss/fonts', {'Host':'www.apple.com'}],
    ['password/verify', {'Host':'iforgot.apple.com'}],
    # ['static/cssj', {'Host':'iforgot.apple.com'}],
    # ['static/jsj', {'Host':'iforgot.apple.com'}],
    # ['images/global', {'Host':'iforgot.apple.com'}],
]

resp_headers = [
    ['etup/ws/1/validate', {'Access-Control-Allow-Origin': 'https://www.ilocal.dd', 'Access-Control-Allow-Credentials': 'true'}],
    ['', {'Accept-Encoding':'gzip, deflate'}],
]

req_body = [ 
]

resp_body = [
        # # ['', 'https', 'http']
        ['', '<meta http-equiv="Content-Security-Policy"', '<!--<meta http-equiv="Content-Security-Policy"'],
        ['', '*.icloud-content.com">', '*.icloud-content.com">-->'],
        ['', 'AutoFillDomain="'+domain, 'AutoFillDomain="icloud.com'],
        ['', '"use strict";', ''],
]

block_paths = [
    '/reportStats',
    '/reportRaw',
    '/jslog',
]

get_cookie = [
]
