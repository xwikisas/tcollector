#!/usr/bin/python

import time
import sys
from collectors.lib import ntplib

COLLECTION_INTERVAL = 60  # seconds
NTP_SERVER = 'ntp.ovh.net'

def main():
  client = ntplib.NTPClient()
  while True:
     ts = int(time.time())

     response = client.request(NTP_SERVER, version=3)
     print ("sys.time.ntp_offset %d %.5f"
        % (ts,response.offset))

     sys.stdout.flush()
     time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
  sys.exit(main())


