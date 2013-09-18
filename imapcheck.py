#!/usr/bin/python
# -*- coding: utf-8 -*-
## Version 0.5

import getpass, imaplib
import time
import ConfigParser
import os


def main():
    # Read configuration
    Config = ConfigParser.ConfigParser()
    try:
        # Make it to read from install dir
        Config.read(os.path.dirname(os.path.realpath(__file__)) + '/imapcheck.cfg')
    except:
        print 'Could not read config file'
        return 0

    # check if correct config
    username = Config.get('account', 'username')
    password = Config.get('account', 'password')
    server = Config.get('account', 'server')
    # Checks
    check_interval = Config.getint('checks', 'check-interval')
    folders_to_check = Config.get('checks', 'folders').split(',')

    M = imaplib.IMAP4_SSL(server)
    M.login(username, password)
    
    # After login clear password variable
    password = ''


    # Get unseened by uid
    # TODO: get last unseened and store uid if newer notify
    # Make cache for last message id
    stored_last_uid = {} 
    for folder in folders_to_check:
        stored_last_uid[folder] = None

    while (True):
        for folder in folders_to_check:
            M.select(folder)
            # Todo massage should be unseen and older then script start time
            typ, data = M.uid('search',None, 'UnSeen')
            if data[0]:
                uids= data[0].split()
                last_uid = uids[-1]
                print last_uid
                if last_uid != stored_last_uid[folder]:
                    stored_last_uid[folder] = last_uid
                    new_message(folder)
                    # Execute command
                print stored_last_uid[folder]
                # if you do it you mark message as read :/
                #typ, data = M.uid('fetch',stored_last_uid[folder], '(RFC822)')
                #print 'Message %s\n%s\n' % (stored_last_uid[folder], data[0][1])
                
            else:
                print 'all read'

        time.sleep(check_interval)

    M.close()
    M.logout()

def new_message(folder):
    import subprocess
    # Do whatever you want
    # TODO: move this function to separate file, for easier upgrades of script
    print "New message in folder" + folder


if __name__ == "__main__":
    main()

