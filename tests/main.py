from context import PythonDNS
from PythonDNS.InterceptResolver import InterceptResolver
from dnslib.server import DNSLogger, DNSServer
import argparse, time

#import ptvsd
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

local_addr = "0.0.0.0"
local_port = 53
upstream_addr = "1.1.1.1"
upstream_port = 53
cloakfile = "cloak.txt"
blacklistfile = "blacklist.txt"
upstream_timeout = 5

print("Starting PythonDNS (%s:%d -> %s:%d)" % (
    local_addr, local_port,
    upstream_addr, upstream_port))

logger = DNSLogger("+request,+reply,+data")

resolver = InterceptResolver(
    upstream_addr,
    upstream_port,
    cloakfile,
    blacklistfile,
    upstream_timeout)

print("<%d CloakRules Imported>" % len(resolver.cloakrules))
print("<%d BlacklistRules Imported>" % len(resolver.blacklistrules))

udp_server = DNSServer(
    resolver,
    address=local_addr,
    port=local_port,
    logger=logger)

udp_server.start_thread()

while udp_server.isAlive():
    time.sleep(1)

