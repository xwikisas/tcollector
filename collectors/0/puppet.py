#!/usr/bin/python

import sys
import time
from subprocess import check_output as qx

COLLECTION_INTERVAL = 300  # seconds
def main():
  while True:
     ts = int(time.time())
     
     last_date = qx(["-c", "grep -h puppet-agent /var/log/syslog.1 /var/log/syslog.0 /var/log/syslog 2> /dev/null | grep 'Finished catalog run' | tail -1 | sed 's/  / /' |cut -d' ' -f1,2,3" ], shell=True)
     last_date_timestamp = qx(["-c", "date --date='" + last_date + "' +%s"], shell=True)
     current_timestamp = qx(["-c", "date +%s"], shell=True)
     difference = int(current_timestamp) - int(last_date_timestamp)
     print ("puppet.lastrun.minutes %d %s"
        % (ts,int(difference/60)))
     

     sys.stdout.flush()
     time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
  sys.exit(main())

