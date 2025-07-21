#!/usr/bin/env python3
import sys
import codecs

payload_file = sys.argv[1]

payload = []
with open(f"{payload_file}", "r") as fd:
    for line in fd:
        linebytes = codecs.escape_decode(bytes(line[0:-1], "latin-1"))[0]
        payload.append(linebytes)

sys.stdout.buffer.write(b"".join(payload))
