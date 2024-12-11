#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import helpers.documents
import helpers.cookie

from markdownify import markdownify
from collections import namedtuple
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def convert(args):
    """Convert a local document to markdown from its id
    """

    document_id = args.id

    logger.debug("Convert html document to markdown [id: %s]", document_id)

    # Open document with BeautifulSoup
    document_raw_html_path = helpers.documents.get_document_raw_html_path(document_id)

    with open(document_raw_html_path, 'r', encoding='utf-8') as f:
        rawSoup = BeautifulSoup(f, 'html.parser')

    # Convert to markdown
    rawMd = markdownify(str(rawSoup.body))

    # Init the header
    header = ""

    # Fill in the header with metadatas from the skeazo cookie, html and user inputs
    Metadata = namedtuple('Metadata', ['prompt', 'cookie_field', 'default_value'])

    with helpers.cookie.Cookie(document_id) as cookie:
        metadatas = {
            'title': Metadata("Titre du document", helpers.cookie.Cookie.TITLE, rawSoup.title.text.replace('\n', '') or ''),
            'author': Metadata("Auteur", helpers.cookie.Cookie.AUTHOR, ''),
            'publication': Metadata("Date de publication", helpers.cookie.Cookie.PUBLICATION, ''),
            'source_name': Metadata("Nom de la source", helpers.cookie.Cookie.SOURCE_NAME, ''),
            'source_uri': Metadata("Uri de la source", helpers.cookie.Cookie.SOURCE_URI, ''),
        }

        for item in ['title', 'author', 'publication', 'source_name', 'source_uri']:
            data = metadatas[item]

            default_value = cookie.get(data.cookie_field, '') or data.default_value

            if default_value:
                value = input("{} ('{}') : ".format(data.prompt, default_value)) or default_value
            else:
                value = input("{} : ".format(data.prompt)) or ''
            
            # Update the header
            header += "{}: {}\n".format(data.cookie_field, value)

            # Update the cookie
            cookie[data.cookie_field] = value

    # Export
    document_raw_md_path = helpers.documents.get_document_raw_md_path(document_id)
    with open(document_raw_md_path, 'w', encoding="utf-8") as fd:
        fd.write('---\n')
        fd.write(header)
        fd.write('---\n')
        fd.write(rawMd)