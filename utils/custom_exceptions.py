#! /usr/bin/env python
# -*- coding: utf-8 -*-


class IPNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class BroadcastFailureError(Exception):
    def __init__(self, message):
        self.message = message


class PingFailureError(Exception):
    def __init__(self, message, *kwargs):
        self.message = message % kwargs


class ArpFailureError(Exception):
    def __init__(self, message):
        self.message = message
