import dnslib
from dnslib import RR, QTYPE, RCODE, DNSRecord
from dnslib.server import BaseResolver, DNSHandler, DNSLogger, DNSServer

from .BlacklistRule import BlacklistRule
from .CloakRule import CloakRule
from .helpers import GetDomainNameFromRequest

class InterceptResolver(BaseResolver):

    def __init__(self, address, port, cloakfile=None, 
        blacklistFile=None, timeout=0):

        self.address = address
        self.port = port
        self.timeout = timeout
        self.cloakrules = []
        self.blacklistrules = []

        if cloakfile:
            self.cloakrules = CloakRule.importRules(cloakfile)

        if blacklistFile:
            self.blacklistrules = BlacklistRule.importRules(
                blacklistFile)

    def blacklist(self, request):

        domain = GetDomainNameFromRequest(request)

        for rule in self.blacklistrules:
            if rule.search(domain):
                return True

        return False

    def cloak(self, request, handler):

        domain = GetDomainNameFromRequest(request)

        for rule in self.cloakrules:
            if rule.search(domain):

                reply = request.reply()
                reply.add_answer(RR(
                    request.questions[0].qname,
                    rtype=QTYPE.CNAME,
                    rdata=dnslib.CNAME(rule.target),
                    ttl=3600
                ))

                subquery = DNSRecord.question(rule.target)
                subresp = self.upstream_resolve(subquery, handler)

                for record in subresp.rr:
                    reply.add_answer(record)

                return reply


    def upstream_resolve(self, request, handler):

        response = request.send(
            self.address,
            self.port,
            timeout=self.timeout
        )

        return DNSRecord.parse(response)


    def resolve(self, request, handler):

        if self.blacklist(request):
            reply = request.reply()
            reply.header.rcode = RCODE.NXDOMAIN
            return reply

        reply = self.cloak(request, handler)

        if reply is None:
            return self.upstream_resolve(request, handler)

        return reply