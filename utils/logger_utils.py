#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging


def get_logger():
    """
    format='%(asctime)s %(message)s'
    :return:
    """
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s %(message)s')
    return logging