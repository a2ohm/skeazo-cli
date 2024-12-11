#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import helpers.documents

logger = logging.getLogger(__name__)

def clean(args):
    document_id = args.id
    document_raw_md_path = helpers.documents.get_document_raw_md_path(document_id)
    document_cleaned_md_path = helpers.documents.get_document_cleaned_md_path(document_id)

    logging.debug("Clean document {}".format(document_id))

    with open(document_raw_md_path, 'r', encoding='utf-8') as file_in:
        document = file_in.read()

    # Currently, do nothing

    with open(document_cleaned_md_path, 'w', encoding='utf-8') as file_out:
        file_out.write(document)