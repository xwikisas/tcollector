#!/usr/bin/python

import sys
import time
import os.path
from subprocess import check_output as qx

COLLECTION_INTERVAL = 300  # seconds
xinit_config_file = '/etc/xinit/xinit.cfg'

if not os.path.isfile(xinit_config_file):
  sys.exit(13)

URL = qx(["-c", "grep CHECK_HTTP_URL= "+xinit_config_file+" | sed 's/CHECK_HTTP_URL=\"//' | sed 's/\"//'" ], shell=True).rstrip()

if URL == '' or URL == '#':
  sys.exit(13)

def main():
  while True:
    ts = int(time.time())
    values = qx(["-c", "curl -o /dev/null --silent " + URL.rstrip() + " -w %{time_connect}:%{time_starttransfer}:%{time_total}"], shell=True)
    svalues= values.split(':')
    print ("xwiki.accesstime.time_connect %d %s"
        % (ts,int(float(svalues[0])*1000)))
    print ("xwiki.accesstime.time_transfer %d %s"
        % (ts,int(float(svalues[1])*1000)))
    print ("xwiki.accesstime.time_total %d %s"
        % (ts,int(float(svalues[2])*1000)))
    sys.stdout.flush()
    time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
  sys.exit(main())
