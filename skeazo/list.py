#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import os
import helpers.documents
import helpers.cookie

logger = logging.getLogger(__name__)

def list(args):

    with os.scandir(helpers.documents.DOCUMENTS_ROOT_PATH) as it :
        for entry in it:
            if entry.is_dir():
                with helpers.cookie.Cookie(entry.name) as cookie:
                    print("{} {} ({})".format(entry.name, cookie.get(helpers.cookie.TITLE), cookie.get(helpers.cookie.AUTHOR)))
