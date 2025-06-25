import sys, logging
import cpppo
from cpppo.server.enip import address, client
host = '10.0.0.3'
port = '44818'
depth = 1
multiple = 0
fragment = False
timeout = 1.0
printing = True
tags = ["LIT301:3"]
with client.connector(host = host, port = port, timeout=timeout) as connection:
    operations = client.parse_operations(tags)
    print "DEBUG ops:",str(tags)
    failures,transactions = connection.process(operations = operations, depth=depth, multiple = multiple, fragment=fragment, printing=printing, timeout=timeout)
    print transactions[0]

