#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
http://www.aboutdebian.com/network.htm

Purpose of this module is to get list of all ip addresses within a local
network.

nmap -sP 192.168.1.*

OR

ping -b your machine's ip address
arp -a  # vi /proc/net/arp

This gives list of all ip addresses except your local machine's ip address.

"""

import re
from subprocess import Popen, PIPE


def get_all_ip_addresses():
    """
    :return:
    """
    status, local_machine_ip_mac = get_ip_address()
    if not status:
        raise Exception("failed to get local machine's ip address.")

    broadcast_ip = local_machine_ip_mac[0][2].rsplit('.', 1)[0]+'.255'
    ping_out, ping_err = ping_broadcast(broadcast_ip)

    if 'WARNING' not in ping_err and ping_err:
        raise Exception("failed to ping broadcast ip.")

    if not check_ping_status(ping_out):
        raise Exception("Unsuccessful ping. 0 packets received.")

    arp_err, arp_out = call_arp()

    if arp_err:
        raise Exception(arp_err)

    pattern = '\?\s*\((\d+\.+\d+\.+\d+\.+\d+)\)\s*at\s*(.*)\s\['

    match = re.findall(pattern, arp_out, re.MULTILINE)

    print '-'*53
    print "| IP Address".ljust(25), '|', "Hardware Address |".rjust(25)
    print '-'*53
    print ("| "+local_machine_ip_mac[0][2]+' (Host)').ljust(25), '|', (local_machine_ip_mac[0][1].strip()+" |").rjust(25)
    for each in match:
        print '-'*53
        print ("| "+each[0]).ljust(25), '|', (each[1]+" |").rjust(25)

    print '-'*53


def call_arp():
    """
    :return:
    """
    try:
        proc = Popen(args=['arp', '-a', '-n'], stdout=PIPE, stderr=PIPE)
        std_out, std_err = proc.communicate()

        return std_err, std_out
    except OSError as ose:
        # print '', ose
        return '', ose


def ping_broadcast(broadcast_ip_addr):
    """
    :param broadcast_ip_addr:
    :return:

    OSError: [Errno 2] No such file or directory

    std_err:  WARNING: pinging broadcast address
    """

    try:
        proc_obj = Popen(args=["ping", "-b", "-c5", broadcast_ip_addr], stdin=PIPE,
                         stdout=PIPE, stderr=PIPE)
        std_out, std_err = proc_obj.communicate()
        # print "std_out: ", std_out
        # print "std_err: ", std_err
        return std_out, std_err
    except OSError as ose:
        # print ose
        return '', ose


def check_ping_status(ping_msg):
    """
    :param ping_msg:
        sample input:
            PING 192.168.0.255 (192.168.0.255) 56(84) bytes of data.
            64 bytes from 192.168.0.5: icmp_seq=3 ttl=64 time=85.3 ms
            64 bytes from 192.168.0.5: icmp_seq=4 ttl=64 time=103 ms

            --- 192.168.0.255 ping statistics ---
            5 packets transmitted, 2 received, 60% packet loss, time 4017ms
            rtt min/avg/max/mdev = 85.339/94.251/103.164/8.917 ms

    r'(\d+\s*)received' - http://stackoverflow.com/a/6092932/3270800
    :return:
    """
    match = re.search(r'(\d+\s*)received', ping_msg, re.MULTILINE)
    if match:
        if int(match.group(1)) > 0:
            return True
        else:
            return False
    else:
        return False


def get_ip_address():
    """
    :return:
    r'^(wlan|eth).*\s*Link\s*encap:Ethernet\s*HWaddr\s*(.*)\n*\s*inet\s*addr:(\d+\.+\d+\.+\d+\.+\d+)
    """

    try:
        proc = Popen(args=["ifconfig"], stdout=PIPE, stderr=PIPE)
        std_out, std_err = proc.communicate()

        reg_pattern = r'^(wlan|eth).*\s*\n*inet\s*addr:(\d+\.+\d+\.+\d+\.+\d+)'
        reg_pattern = r'^(wlan|eth).*\s*Link\s*encap:Ethernet\s*HWaddr\s*(.*)\n*\s*inet\s*addr:(\d+\.+\d+\.+\d+\.+\d+)'
        ip_mac_list = re.findall(reg_pattern, std_out, re.MULTILINE)
        if ip_mac_list:
            return True, ip_mac_list
    except OSError as ose:
        # print ose
        return False, ''


if __name__ == '__main__':

    # ping_broadcast("192.168.0.255")
    # ip = get_ip_address()
    # so, se = ping_broadcast(ip[1].rsplit('.', 1)[0]+'.255')
    # print check_ping_status(so)
    # call_arp()

    get_all_ip_addresses()