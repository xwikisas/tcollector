#!/usr/bin/python

import time
import sys
import os.path
from subprocess import check_output as qx

COLLECTION_INTERVAL = 60  # seconds

def main():
  while True:
     ts = int(time.time())

     root_keys = qx(["-c", "sudo /usr/bin/wc -l /root/.ssh/authorized_keys 2>/dev/null | awk '{print $1}'"], shell=True).rstrip()
     if root_keys == '':
       root_keys = 0
     print ("security.rootkeys %d %s"
        % (ts,root_keys))

     sys.stdout.flush()
     time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
  sys.exit(main())

