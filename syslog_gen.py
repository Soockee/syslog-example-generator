#!/usr/bin/env python3
'''
Syslog Generator

Had a need to generate generic syslog messages to 
test open source logging solutions.
'''

import socket
import argparse
import random
import sys
import time
import logging
from logging import FileHandler
import datetime

"""
Modify these variables to change the hostname, domainame, and tag
that show up in the log messages. 
"""   
hostname = "host"
domain_name = ".example.com"
tag = ["kernel", "python", "ids", "ips"]
syslog_level = ["info", "error", "warning", "critical"]
pri_choice = ["165", "34"]
strdata = "-"
def raw_udp_sender(message, host, port):
    # Stubbed in or later use
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = bytes(message, 'UTF-8')
        send = sock.sendto(message, (host, port))
    finally:
        sock.close()

def open_sample_log(sample_log):
    try:
        with open(sample_log, 'r') as sample_log_file:
            random_logs = random.choice(list(sample_log_file))
            return random_logs
    except FileNotFoundError:
        print("[+] ERROR: Please specify valid filename")
        return sys.exit()

def syslogs_sender():
    # Initalize SysLogHandler
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    syslog = FileHandler('example.log')
    logger.addHandler(syslog)
    msg_id = 1

    for message in range(1, args.count+1):
        # Randomize some fields
        random_host = random.choice(range(1,11))
        random_appname = random.choice(tag)
        random_level = random.choice(syslog_level)
        fqdn = "{0}{1}{2}".format(hostname, random_host, domain_name)
        random_pid = random.choice(range(500,9999))
        random_msgid= random.choice(range(500,9999))
        structured_data = '[example@32457] iut="3"'
        pri = random.choice(pri_choice)
        version = 4


        message = open_sample_log(args.file)
        fields = {
            'pri_field': pri,
            'version_field': version,
            'host_field': fqdn, 
            'date_field': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'tag_field': random_appname,
            'msg_field': msg_id
        }
	
        format = logging.Formatter\
                ('<%(pri_field)s>%(version_field)s %(date_field)s %(host_field)s {0} {1} ID%(msg_field)s {2} %(message)s'\
                .format(random_appname, random_pid, strdata))
        syslog.setFormatter(format)
			
        msg_id = msg_id + 1
        getattr(logger, random_level)(message, extra=fields)

    logger.removeHandler(syslog)
    syslog.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, 
                        help="Read messages from file")
    parser.add_argument("--count", type=int, required=True,
                        help="Number of messages to send")
    parser.add_argument("--sleep", type=float, help="Use with count flag to \
                        send X messages every X seconds, sleep being seconds")
	
    args = parser.parse_args()
		
    if args.sleep:
        print("[+] Sending {0} messages every {1}"\
            .format(args.count, args.sleep, args.host, args.port))
        try:
            while True:
                syslogs_sender()
                time.sleep(args.sleep)
        except KeyboardInterrupt:
            # Use ctrl-c to stop the loop
            print("[+] Stopping syslog generator...")
    else:
        print("[+] Sending {0} messages".format
            (args.count))
        syslogs_sender()
