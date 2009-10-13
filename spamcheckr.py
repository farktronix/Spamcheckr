#!/usr/bin/python
# Checks your gmail spam mailbox and prints out the most frequently spammed email addresses. 
# Useful for cleaning up catch-all addresses.

import imaplib
import sys
from email.parser import HeaderParser
from operator import itemgetter

def usage():
    print "Usage: %s user pass\n" % sys.argv[0]

def printAddrs(addrs):
    sort = sorted(addrs.items(), key=itemgetter(1)) 
    for addr in sort:
        print "%s %s" % (addr[1], addr[0])

user = sys.argv[1]
password = sys.argv[2]

if user is None or password is None:
    usage()

gmail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
gmail.login(user, password)
gmail.select("[Gmail]/Spam", True)
typ, msglist = gmail.search(None, "ALL")
addrs = {}
parser = HeaderParser()
try:
    for msgid in msglist[0].split():
        typ, emails = gmail.fetch(msgid, '(BODY[HEADER])')
        for email in emails:
            if len(email) < 2:
                continue 
            msg = parser.parsestr(email[1])
            to = msg.get("To")
            if to is None:
                continue
            for addr in to.split(","):
                if addr not in addrs:
                    count = 1
                else:
                    count = addrs[addr] + 1
                addrs[addr] = count
except Exception:
    printAddrs(addrs)
    gmail.logout()
    raise
printAddrs(addrs)
gmail.logout()

