# CipherGinx &nbsp; ![GitHub release (latest by date)](https://img.shields.io/github/v/release/cipheras/cipherginx?style=flat-square&logo=superuser)
#### Advanced phishing tool used for session & credential grabbing and bypassing 2FA using man-in-the-middle attack with standalone reverse proxy server. 

![Lines of code](https://img.shields.io/tokei/lines/github/cipheras/cipherginx?style=flat-square)
&nbsp;&nbsp;&nbsp;&nbsp;![Python version](https://img.shields.io/badge/python-3.X-green?style=flat-square&labelColor=grey&color=darkgreen)
&nbsp;&nbsp;&nbsp;&nbsp;![Code Quality](https://img.shields.io/badge/dynamic/json?url=https://jsonkeeper.com/b/KNO7&label=code%20quality&query=codequality&style=flat-square&labelColor=grey&color=yellowgreen)
&nbsp;&nbsp;&nbsp;&nbsp;![platform](https://img.shields.io/badge/dynamic/json?url=https://jsonkeeper.com/b/KNO7&label=platform&query=platform&style=flat-square&labelColor=grey&color=purple)

![example](../asset/screen.png?raw=true)

## Description
This tool is used for advanced phishing attacks using reverse proxy. It can also bypass **2FA** or **2-factor authorization**. Captured tokens will be written in the file `token.txt` on successful phish. Attack can use this tool to phish any website by creating a suitable configuration. Author has already tested it with **gmail, outlook & icloud**, however no orginal config has been uploaded here for security purposes. This tool is only to be used as a POC to understand advanced phishing and for **Red Teaming** purposes.
<br>

#### Advantages over other similar tools:
- This tool lets you modify anything in the website to be used for phishing. 
- Other tools have restriction like you can not replace **response headers or request body**, or you need to use third party tools along with them. 
- You can also block certain paths. Tool returns `[200 ok]` response to those paths without any body, to avoid any suspicion.
- Supports **regex**.
- Comparably smaller config files because of path based modification and fast to make. 
- You do not have to enter whole URL path in the `config.py` files. You can just enter part of URL path and tool will automatically match it.


## Options
```
cipherginx.py [-h] [-v] [-l {info,debug,error}] [config]

positional arguments:
  config                select config to run

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show tool version
  -l {info,debug,error}, --level {info,debug,error}
                        logging level

Example:
cipherginx.py myconfig -l debug
or
cipherginx.py -l debug myconfig
```

## Usage
*In order to use this tool `python3` is required.* 
To install python in windows get it from [here](https://www.python.org/downloads/).
<br>
- For help type `python cipherginx -h`.
- If you are using port 443(for ssl/tls), run tool with `sudo`.
- Use your own cert for **ssl/tls** & put it in `cert` folder with name `server.pem`.
- Given cert can be used but it is **unsigned**.
- Put your `config.py` files in config folder.

## Config Structure
Config files are structured as sub lists inside a list with two/three items, where first item is the `path` on which that particular task is to be executed.
<br>
Each sublist acts as task. For each replacement you have to add one sublist.
<br>
`path` can be just some part of the URL where the task is to be executed.
<br>
Use `'' (blank single quotes)` if you want to apply that replacement on all the URLs.
<br>

**Basic configuration:**
variable|use
-|-
`hostname` | {target website}
`isSSL`    | {http or https}
`server`   | {your domain}
`port`     | {port to run on}
<br>

**Phishing configuration:**
&emsp;list|&emsp;&emsp;&emsp;&emsp;use
-|-
`inject_domain` |&emsp; [domain to be replaced, domain to be replaced with] 
`req_headers`   |&emsp; [path, headers in dict format]
`resp_headers`  |&emsp; [path, headers in dict format]
`req_body`      |&emsp; [path, string to be replaced, string to be replaced with]
`resp_body`     |&emsp; [path, string to be replaced, string to be replaced with]
`block_paths`   |&emsp; [paths]
`get_cookie`    |&emsp; [cookie names]

## Disclaimer
*This tool is merely a POC of what attackers can do. Author is not responsible for any use of this tool in any nefarious activity.*

## License
**cipherginx** is made by **@cipheras** and is released under the terms of the &nbsp;![GitHub License](https://img.shields.io/github/license/cipheras/cipherginx?color=darkgreen)

## Contact &nbsp; [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fcipheras%2Fcipherginx&label=Tweet)](https://twitter.com/intent/tweet?text=Hi:&url=https%3A%2F%2Fgithub.com%2Fcipheras%2Fcipherginx)
> Feel free to submit a bug, add features or issue a pull request.


