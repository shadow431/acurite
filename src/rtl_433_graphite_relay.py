#!/usr/bin/env python

"""Graphite(Carbon) monitoring relay for rtl_433."""

# Start rtl_433 (rtl_433 -F syslog::1433), then this script

# Option: PEP 3143 - Standard daemon process library
# (use Python 3.x or pip install python-daemon)
# import daemon

from __future__ import print_function
from __future__ import with_statement

import socket
import time
import json
import os

UDP_IP = "0.0.0.0"
UDP_PORT = 1433

#get GRAPHITE_HOST from environment 
GRAPHITE_HOST = os.environ.get('GRAPHITE_HOST', '127.0.0.1')
GRAPHITE_PORT = os.environ.get('GRAPHITE_PORT', 2003)
GRAPHITE_PREFIX = os.environ.get('GRAPHITE_PREFIX', 'rtlsdr.')

class GraphiteTcpClient(object):
    def __init__(self, host='localhost', port=2003, ipv6=False):
        """Create a new client."""
        fam = socket.AF_INET6 if ipv6 else socket.AF_INET
        family, _, _, _, addr = socket.getaddrinfo(
            host, port, fam)[0]
        self._addr = addr
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect(self._addr)

    def _send(self, message):
        """Send raw data to graphite."""
        """convert message to bytes"""
        message = bytes(message, 'utf-8')
        try:
            self._sock.send(message)
        except (socket.error, RuntimeError):
            pass

    def push(self, path, value, timestamp=None):
        """Send a value to graphite."""
        if not timestamp:
            timestamp = int(time.time())

        message = "{0} {1} {2}\n".format(path, value, timestamp)
        self._send(message)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind((UDP_IP, UDP_PORT))


def sanitize(text):
    return text.replace(" ", "_").replace("/", "_").replace(".", "_").replace("&", "")


def parse_syslog(line):
    """Try to extract the payload from a syslog line."""
    line = line.decode("ascii")  # also UTF-8 if BOM
    if line.startswith("<"):
        # fields should be "<PRI>VER", timestamp, hostname, command, pid, mid, sdata, payload
        fields = line.split(None, 7)
        line = fields[-1]
    return line


def rtl_433_probe():
    print("Probe starting")
    graphite = GraphiteTcpClient(host=GRAPHITE_HOST,
                                 port=GRAPHITE_PORT)
    
    data_types = ["humidity", "battery_ok", "wind_avg_km_h", "wind_dir_deg", "temperature_F","temperature_C","rain_in"]

    while True:
        line, addr = sock.recvfrom(1024)

        try:
            line = parse_syslog(line)
            data = json.loads(line)
            now = int(time.time())
            print(data)
            label = sanitize(data["model"])
            if "channel" in data:
                label += ".CH" + str(data["channel"])
            if "id" in data:
                label += ".ID" + str(data["id"])
            path = GRAPHITE_PREFIX + label

            for data_type in data_types:
                if data_type in data:
                    graphite.push(path + '.' + data_type, data[data_type], now)
            """
            if "battery_ok" in data:
                graphite.push(path + '.battery', data["battery_ok"], now)

            if "humidity" in data:
                graphite.push(path + '.humidity', data["humidity"], now)

            graphite.push(path + '.temperature', data["temperature_C"], now)
            """
            #graphite.commit()  # for Pickle protocol only

        except KeyError:
            pass

        except ValueError:
            pass


def run():
    # with daemon.DaemonContext(files_preserve=[sock]):
    #  detach_process=True
    #  uid
    #  gid
    #  working_directory
    print("Running Probe")
    rtl_433_probe()


if __name__ == "__main__":
    print("Starting rtl_433_graphite_relay.py")
    print("GRAPHITE_HOST: " + GRAPHITE_HOST)
    print("GRAPHITE_PORT: " + GRAPHITE_PORT)
    print("GRAPHITE_PREFIX: " + GRAPHITE_PREFIX)
    run()