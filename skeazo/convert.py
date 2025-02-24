#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import helpers.documents
import helpers.cookie
import helpers.index

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

    # Collect metadata
    Metadata = namedtuple('Metadata', ['prompt', 'cookie_field', 'default_value'])

    with helpers.cookie.Cookie(document_id) as cookie:
        metadata = {
            'title': Metadata("Titre du document", helpers.cookie.TITLE, rawSoup.title.text.replace('\n', '') or ''),
            'author': Metadata("Auteur", helpers.cookie.AUTHOR, ''),
            'publication': Metadata("Date de publication", helpers.cookie.PUBLICATION, ''),
            'source_name': Metadata("Nom de la source", helpers.cookie.SOURCE_NAME, ''),
            'source_uri': Metadata("Uri de la source", helpers.cookie.SOURCE_URI, ''),
        }

        for item in ['title', 'author', 'publication', 'source_name', 'source_uri']:
            entry = metadata[item]

            default_value = cookie.get(entry.cookie_field, '') or entry.default_value

            if default_value:
                value = input("{} ('{}') : ".format(entry.prompt, default_value)) or default_value
            else:
                value = input("{} : ".format(entry.prompt)) or ''

            # Update the cookie
            cookie[entry.cookie_field] = value

    # Convert to markdown
    rawMd = markdownify(str(rawSoup.body))

    # Export the markdown file
    document_raw_md_path = helpers.documents.get_document_raw_md_path(document_id)
    with open(document_raw_md_path, 'w', encoding="utf-8") as fd:
        fd.write(rawMd)

    # Add the document to the index
    index = helpers.index.Index()
    
    with helpers.cookie.Cookie(document_id) as cookie:
        index.add_document(document_id, cookie)