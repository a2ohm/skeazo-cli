#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import os
import helpers.documents
import helpers.cookie
import helpers.index

logger = logging.getLogger(__name__)

def list(args):
    index = helpers.index.Index()

    for document in index.list_all_documents():
        print(f"{document.id} {document.title} ({document.author})")
