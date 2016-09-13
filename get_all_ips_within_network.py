#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
http://www.aboutdebian.com/network.htm

Purpose of this module is to get list of all IP and MAC addresses within a
network.

Steps followed to achieve this are:

1) Get host machine's IP address.
2) Generate broadcast IP using host's IP address.
3) Ping broadcast IP address.
4) Validate Ping response.
5) Call arp command to get list of all IP and MAC address.

Sample:
    1) ifconfig - 192.168.0.10
    2) ping -b -c5 192.168.0.255
    3) arp -a -n

arp doesn't include host machine's IP and MAC address. That's why we have
added host's IP and MAC address using command 'ifconfig' result.


nmap -sP 192.168.0.*
"""

import re
from subprocess import Popen, PIPE


def get_ip_mac_address():
    """
    command - ifconfig
    parsing commands output to get valid ip and mac address from eth or wlan.

    :return: ip and mac address.

    """

    try:
        proc = Popen(args=["ifconfig"], stdout=PIPE, stderr=PIPE)
        std_out, std_err = proc.communicate()

        reg_pattern = r'^(wlan|eth).*\s*Link\s*encap:Ethernet\s*HWaddr\s*(.*)\n*\s*inet\s*addr:(\d+\.+\d+\.+\d+\.+\d+)'
        ip_mac_list = re.findall(reg_pattern, std_out, re.MULTILINE)
        if ip_mac_list:
            return True, ip_mac_list
    except OSError as ose:
        # log ose
        return False, ''


def ping_broadcast(broadcast_ip_addr):
    """
    command - ping -b -c5 broadcast_ip_addr

    :param broadcast_ip_addr: broadcast ip address.
    :return: ping status.

    """

    try:
        proc_obj = Popen(args=["ping", "-b", "-c5", broadcast_ip_addr],
                         stdin=PIPE, stdout=PIPE, stderr=PIPE)
        std_out, std_err = proc_obj.communicate()

        return std_out, std_err
    except OSError as ose:
        # log ose
        return '', ose


def check_ping_status(ping_response):
    """
    :param ping_response: ping command response.
    :return: ping success status.
    """
    match = re.search(r'(\d+\s*)received', ping_response, re.MULTILINE)
    if match:
        if int(match.group(1)) > 0:
            return True
        else:
            return False
    else:
        return False


def call_arp():
    """
    command - arp -a -n
    :return: raw output of arp command having list of ip and mac addresses.
    """
    try:
        proc = Popen(args=['arp', '-a', '-n'], stdout=PIPE, stderr=PIPE)
        std_out, std_err = proc.communicate()

        return std_err, std_out
    except OSError as ose:
        # log ose
        return '', ose


def get_all_ip_addresses():
    """
    Calls functions based on the follow of execution steps mentioned on the
    top of module.
    Parses the output of arp command output and displays table view of list of
    ip and mac address.

    :return: ip and mac table view.
    """
    status, local_machine_ip_mac = get_ip_mac_address()
    if not status:
        raise Exception("failed to get local machine's ip address.")

    broadcast_ip = local_machine_ip_mac[0][2].rsplit('.', 1)[0]+'.255'
    ping_out, ping_err = ping_broadcast(broadcast_ip)

    if 'WARNING' not in ping_err and ping_err:
        raise Exception("failed to ping broadcast ip.")

    if not check_ping_status(ping_out):
        raise Exception("Unsuccessful ping. 0 packets received for broadcast "
                        "ip address - %s."%broadcast_ip)

    arp_err, arp_out = call_arp()

    if arp_err:
        raise Exception(arp_err)

    pattern = '\?\s*\((\d+\.+\d+\.+\d+\.+\d+)\)\s*at\s*(.*)\s\['

    match = re.findall(pattern, arp_out, re.MULTILINE)

    print '-'*53
    print "| IP Address".ljust(25), '|', "Hardware Address |".rjust(25)
    print '-'*53

    print ("| "+local_machine_ip_mac[0][2]+' (Host)').ljust(25), '|', \
        (local_machine_ip_mac[0][1].strip()+" |").rjust(25)

    for each in match:
        print '-'*53
        print ("| "+each[0]).ljust(25), '|', (each[1]+" |").rjust(25)

    print '-'*53


if __name__ == '__main__':

    get_all_ip_addresses()
