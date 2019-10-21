from context import PythonDNS
from PythonDNS.InterceptResolver import InterceptResolver
from dnslib.server import DNSLogger, DNSServer

#import ptvsd
#
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

import argparse, time

p = argparse.ArgumentParser(prog="PythonDNS")

p.add_argument("-la",
    "--local_address",
    type=str,
    default="",
    nargs="?",
    metavar="local address",
    help="Local listen address")

p.add_argument("-lp",
    "--local_port",
    type=int,
    default=53,
    nargs="?",
    metavar="local port",
    help="Local listen port")

p.add_argument("upstream_address",
    type=str,
    metavar="<upstream_address>",
    help="Upstream DNS address")

p.add_argument("-up",
    "--upstream_port",
    type=int,
    default=53,
    nargs="?",
    metavar="<upstream_port>",
    help="Upstream DNS port")

p.add_argument("-t",
    "--upstream_timeout",
    type=int,
    default=5,
    nargs="?",
    metavar="<upstream_timeout>",
    help="Upstream timeout (seconds)")

p.add_argument("-c",
    "--cloakfile",
    type=str,
    default=None,
    metavar="cloak file",
    help="File path to cloak file")

p.add_argument("-b",
    "--blacklistfile",
    type=str,
    default=None,
    metavar="blacklist file",
    help="File path to blacklist file")

p.add_argument("-d",
    "--debug",
    type=bool,
    default=False,
    nargs="?",
    metavar="<debug>",
    help="Enable debugging")


args = p.parse_args()



print("Starting PythonDNS (%s:%d -> %s:%d)" % (
    args.local_address, args.local_port,
    args.upstream_address, args.upstream_port))

logger = DNSLogger("+request,+reply,+data")

resolver = InterceptResolver(
    args.upstream_address,
    args.upstream_port,
    args.cloakfile,
    args.blacklistfile,
    args.upstream_timeout)

print("<%d CloakRules Imported>" % len(resolver.cloakrules))
print("<%d BlacklistRules Imported>" % len(resolver.blacklistrules))

udp_server = DNSServer(
    resolver,
    port=args.local_port,
    address=args.local_address,
    logger=logger)

udp_server.start_thread()

while udp_server.isAlive():
    time.sleep(1)

