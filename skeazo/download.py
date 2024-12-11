#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import os
import requests
import helpers.documents
import helpers.cookie

logger = logging.getLogger(__name__)

def download(args):
    """Download a document from an url
    """

    document_url = args.url
    document_id = helpers.documents.get_document_id_from_url(document_url)

    logger.debug("Download a document from an url: %s [id: %s]", document_url, document_id)

    # Create document directory
    document_directory_path = helpers.documents.get_document_directory_path(document_id)

    if not os.path.isdir(document_directory_path):
        os.mkdir(document_directory_path)

    # Save url into cookie
    with helpers.cookie.Cookie(document_id) as cookie:
        cookie[helpers.cookie.Cookie.SOURCE_URI] = document_url

    # Download document
    document_raw_html_path = helpers.documents.get_document_raw_html_path(document_id)

    # Download the raw document from an url
    # and save it to a file
    # cf. https://docs.python-requests.org/en/latest/user/quickstart/#raw-response-content

    try:
        r = requests.get(document_url, stream=True, timeout=1)
        encoding = r.apparent_encoding

        with open(document_raw_html_path, 'w', encoding="utf-8") as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk.decode(encoding, 'ignore'))

        print("ID: {}".format(document_id))
        return True
    
    except requests.ConnectTimeout:
        logger.debug("URL inaccessible (timeout), check your internet connection")
        return False
    
    except requests.ConnectionError:
        logger.debug("URL inaccessible (connection error), check your internet connection")
        return False