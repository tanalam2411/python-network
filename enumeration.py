#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enumeration classes.
"""


class Commands(object):
    arp = ['arp', '-a', '-n']
    ifconfig = "ifconfig"
    ping_broadcast = ["ping", "-b", "-c10"]
