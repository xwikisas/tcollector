#!/usr/bin/python
import sys
import time
import os.path
import re
from subprocess import check_output as qx

# XWiki-specific metric gathering script
# Available metrics:
#
# xwiki.accesstime.time_connect
# xwiki.accesstime.time_transfer
# xwiki.accesstime.time_total
# xwiki.xinit.proccron.missing (or commented)
# xwiki.xinit.httpcron.missing (or commented)
# xwiki.xinit.mailparam.missing
# xwiki.xinit.maintenance
# xwiki.xinit.lastrun
#

COLLECTION_INTERVAL = 300  # seconds
xinit_config_file = '/etc/xinit/xinit.cfg'

if not os.path.isfile(xinit_config_file):
  sys.exit(13)

if not os.path.islink('/usr/local/xwiki') or not os.path.isdir('/usr/local/xwiki'):
  sys.exit(13)

URL = ''
for line in open(xinit_config_file).readlines():
  m = re.search('(#?)CHECK_HTTP_URL="(.*)"', line)
  if m and m.group(1) != '#':
    URL = m.group(2)

def main():
  while True:
    ts = int(time.time())
    
    # Config parsing stuff
    URL = ''
    mailparam_missing = 1
    for line in open(xinit_config_file).readlines():
      m = re.search('(#?)CHECK_HTTP_URL="(.*)"', line)
      if m and m.group(1) != '#':
        URL = m.group(2)
      m = re.search('(#?)MAIL="(.*)"', line)
      if m and m.group(1) != '#' and m.group(2) != '':
        mailparam_missing = 0


    # Access time section (URL computed each time in order to allow live config edits without needing to restart tcollector)
    if URL != '':
      values = qx(["-c", "curl -o /dev/null --silent " + URL.rstrip() + " -w %{time_connect}:%{time_starttransfer}:%{time_total}"], shell=True)
      svalues= values.split(':')
      print ("xwiki.accesstime.time_connect %d %s"
        % (ts,int(float(svalues[0])*1000)))
      print ("xwiki.accesstime.time_transfer %d %s"
        % (ts,int(float(svalues[1])*1000)))
      print ("xwiki.accesstime.time_total %d %s"
        % (ts,int(float(svalues[2])*1000)))

    # Mailparam section
    print ("xwiki.xinit.mailparam.missing %d %d"
        % (ts,mailparam_missing))

    # Maintenance section
    xinitmaintenance = 0
    if os.path.isfile('/etc/xinit/maintenance'):
      xinitmaintenance = 1
    print ("xwiki.xinit.maintenance %d %d"
        % (ts,xinitmaintenance))

    # Crons section
    if os.path.isfile('/var/spool/cron/crontabs/root'):
      proccron_missing = 1
      httpcron_missing = 1
      for line in open('/var/spool/cron/crontabs/root').readlines():
        m = re.search('(#?).*/etc/init.d/xwiki.sh check-proc.*', line)
        if m and m.group(1) != '#':
          proccron_missing = 0
        m = re.search('(#?).*/etc/init.d/xwiki.sh check-http.*', line)
        if m and m.group(1) != '#':
          httpcron_missing = 0
      print ("xwiki.xinit.proccron.missing %d %d"
        % (ts,proccron_missing))
      print ("xwiki.xinit.httpcron.missing %d %d"
        % (ts,httpcron_missing))

    # XInit last run section
    xinit_lastrun = qx(["-c", "tail -1 /var/log/xinit.log | cut -d' ' -f1,2 | sed -e 's/^\([0-9]*\)-\([0-9]*\)-\([0-9]*\)/\\3-\\2-\\1/'"], shell=True)
    xinit_lastrun_timestamp = qx(["-c", "date --date='" + xinit_lastrun + "' +%s"], shell=True)    
    print ("xwiki.xinit.lastrun %d %d"
	% (ts,(ts-int(xinit_lastrun_timestamp))/60))
    
    sys.stdout.flush()
    time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
  sys.exit(main())

