#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

"""

import ConfigParser

config_file_name = 'default.conf'


config = ConfigParser.ConfigParser()
config.read(config_file_name)


def get_config_option(section_name, option_name):
    """
    :param section_name:
    :param option_name:
    :return: config option value.
    """

    if config.has_option(section_name, option_name):
        return config.get(section_name, option_name)
    return None

if __name__ == '__main__':

    print get_config_option('Patterns', 'IpMacRegex')
