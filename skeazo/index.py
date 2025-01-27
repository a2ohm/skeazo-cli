#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import helpers.index

def do_action(args):
    """Possible actions:
    - init: initialize the index
    """

    if args.action == 'init':
        helpers.index.init_index()