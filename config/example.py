#! /usr/bin/env python3

hostname = 'xyz.com'
isSSL    = True
server   = 'localhost'
port     = 443
domain   = server if port in [443,80] else '{}:{}'.format(server,port)

inject_domain = [
    ['sub.xyz.com', 'sub.'+domain],
    ['dom.xyz.com', 'dom.'+domain],
]

req_headers = [
    ['', {'Connection':'close'}],
    ['/js/example.js', {'Host':'sub.xyz.com'}],
    ['/static', {'Host':'sub.xyz.com'}],
]

resp_headers = [
    ['', {}]
]

req_body = [
    ['klajndf/alif/akjdf', 'original', 'replaced'],
]

resp_body = [
    # # ['', 'https', 'http'],
    ['', 'string to be replaced', 'string to be replaced with'],
    ['/signin', 'Sign in', 'Hack it'],
]

block_paths = [
    '/cspreport',
]

get_cookie = [
    'ID',
    'TOKEN',
]

