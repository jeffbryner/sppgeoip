#!/usr/bin/python2
import os
import GeoIP
import sys

try:
    ipAddress=os.environ["TCPREMOTEIP"]
    gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    #determine country
    sourceCountry=str(gi.country_code_by_addr(ipAddress)) +": " + str(gi.country_name_by_addr(ipAddress))
    
    sys.stderr.write('Caller is from : ' + sourceCountry +'\n')
    sys.stdout.write('HX-SPP-GEOIP: ' + sourceCountry +'\n')
except KeyError:
    sys.stderr.write(sys.argv[0] + ": No $TCPREMOTEIP environment variable set..quitting\n")
    sys.exit(1)
    