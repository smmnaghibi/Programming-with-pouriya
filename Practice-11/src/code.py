#! /usr/bin/env python3

from xml.dom import minidom
import logging
from sys import argv
from time import sleep
import signal
import os


log_level = logging.INFO
if "--debug" in argv:
    log_level = logging.DEBUG
logging.getLogger().setLevel(log_level)

flag = True
def level(sig, frame):
    global flag, log_level
    if flag and log_level != logging.DEBUG:
        log_level = logging.DEBUG
        logging.getLogger().setLevel(log_level)
    else:
        log_level = logging.INFO
        logging.getLogger().setLevel(log_level)
    flag = not flag



def read_config(filename, mandatory_key_list, cfg):
    file = minidom.parse(os.getcwd()+"/src/"+filename)
    users = file.getElementsByTagName('user')

    file_key = []
    for k in users:
        file_key.append(k.attributes['name'].value)
    logging.debug("Line : ")
    for elem in users:
        logging.debug("Key : " + elem.attributes['name'].value + " And Value : " + elem.firstChild.data)
        cfg[elem.attributes['name'].value] = elem.firstChild.data

    for mandatory_key in mandatory_key_list:
        if mandatory_key not in file_key:
            return False, 'Could not found "' + mandatory_key + '"'
    return True, cfg



while True:
    signal.signal(signal.SIGINT, level)
    status, result = read_config('file.xml',['first-name','last-name'],{'middle-name':''})
    if not status:
        logging.error(result)
        exit(1)
    cfg = result
    logging.info("Your name is " + cfg['first-name'] + ' ' + cfg['middle-name'] + ' ' + cfg['last-name'])

    sleep(10)
