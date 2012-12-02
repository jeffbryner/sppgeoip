#!/usr/bin/python2
import os
import GeoIP
import sys
#import logging
#import logging.handlers
import syslog


#logging is supposed to work automagically via spp, but it doesn't for me
#workaround to create a syslog entry if we block something.

#logger = logging.getLogger('SPPAuth')
#logger.setLevel(logging.DEBUG)
#handler = logging.handlers.SysLogHandler(address = '/dev/log')
#logger.addHandler(handler)


try:
    ipAddress=os.environ["TCPREMOTEIP"]
    gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    #determine country
    sCode=str(gi.country_code_by_addr(ipAddress))
    sName=str(gi.country_name_by_addr(ipAddress))
    sourceCountry= sCode + ": " + sName
    
    sys.stderr.write('Caller is from : ' + sourceCountry +'\n')
    sys.stdout.write('HX-SPP-GEOIP: ' + sourceCountry +'\n')

    authuser=os.environ["SMTPAUTHUSER"]    
    sys.stdout.write('HX-SPP-USER: ' + authuser +'\n')    
    
    #is this ok?
    allowed=['US']
    if sCode not in allowed:
        sys.stderr.write("Caller is from: %s which is not allowed..dropping connection\n"% sourceCountry)
        syslog.syslog("SMTP Auth from: %s %s dropping connection"% (sourceCountry,ipAddress))
        sys.stdout.write('D'+'\n') #drop connection.
        sys.exit(1)
    else:
        syslog.syslog("SMTP Auth from: %s %s allowed"% (sourceCountry,ipAddress))
        sys.exit(0)
    
except KeyError as e:
    sys.stderr.write(sys.argv[0] + ": No environment variable set..quitting\n")
    sys.stderr.write(str(e) + '\n')
    sys.exit(1)
    

