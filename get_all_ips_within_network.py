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

from enumeration import Commands
from conf_reader import get_config_option


def get_ip_mac_address():
    """
    command - ifconfig
    parsing commands output to get valid ip and mac address from eth or wlan.

    :return: ip and mac address.

    """

    try:
        process = Popen(args=[Commands.ifconfig], stdout=PIPE, stderr=PIPE)
        std_out, std_err = process.communicate()

        regex_pattern = get_config_option('Patterns', 'IpMacRegex')
        ip_mac_list = re.findall(regex_pattern, std_out, re.MULTILINE)
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
        args_list = Commands.ping_broadcast
        args_list.append(broadcast_ip_addr)
        process = Popen(args=args_list, stdout=PIPE, stderr=PIPE)
        std_out, std_err = process.communicate()

        return std_out, std_err
    except OSError as ose:
        # log ose
        return '', ose


def check_ping_status(ping_response):
    """
    :param ping_response: ping command response.
    :return: ping success status.
    """

    regex_pattern = get_config_option('Patterns', 'PingStatusRegex')
    match = re.search(regex_pattern, ping_response, re.MULTILINE)
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
        process = Popen(args=Commands.arp, stdout=PIPE, stderr=PIPE)
        std_out, std_err = process.communicate()

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
                        "ip address - %s." % broadcast_ip)

    arp_err, arp_out = call_arp()

    if arp_err:
        raise Exception(arp_err)

    regex_pattern = get_config_option('Patterns', 'ArpRegex')

    match = re.findall(regex_pattern, arp_out, re.MULTILINE)

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
