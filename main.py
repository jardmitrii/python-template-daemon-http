#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include.daemon import Daemon
from include.httprest import runserver
from configuration import pidfile, listen_address, listen_port, log_format, mainlog
from sys import argv
import logging

def usage():
    print """
Script usage parameters:
    debug   - Run script in current console with debug mode.
    start   - Run script as daemon
    stop    - Stop daemon
    restart - Rerun script as daemon
    help    - Show this help
"""

def exit_with_error():
    usage()
    exit(2)

def main():
    try:
        runserver(listen_address, listen_port)
            
    except KeyboardInterrupt:
        exit(0)
    
class MyDaemon(Daemon):
    def run(self):
        logging.debug('Running')
        main()

if __name__ == "__main__":
    logging.basicConfig(format=log_format, level=logging.DEBUG, filename=mainlog)
    daemon = MyDaemon(pidfile)
    actions = { 'debug': main,
                'start': daemon.start,
                'stop': daemon.stop,
                'restart': daemon.restart,
                'help': usage
                }
    
    if len(argv) == 2:
        actions.get(argv[1], exit_with_error)()            
        exit(0)
        
    else:
        exit_with_error()
