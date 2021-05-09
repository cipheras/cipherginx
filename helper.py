#! /usr/bin/env python3

import subprocess as p
import time

RESET     = "\033[0m"
RED       = "\033[31m"
GREEN     = "\033[32m"
LIGHTGREEN = "\033[38;5;106m"
YELLOW    = "\033[33m"
BLUE      = "\033[34m"
PURPLE    = "\033[35m"
CYAN      = "\033[36m"
WHITE     = "\033[37m"
BGBLACK   = "\033[40m"
BGYELLOW  = "\033[43m"
BGGREEN   = "\033[48;5;64m"
BGORANGE  = "\033[48;5;202m"
BGBLUE    = "\033[48;5;26m"
BOLD      = "\033[1m"
UNDERLINE = "\033[4m"
BLINK     = "\033[5m"
CLEAR     = "\033[2J\033[H"

def cwin():
    try:
        p.Popen('',shell=True)
        time.sleep(0.01)
        print(CLEAR)
    except Exception as e:
        print(e)