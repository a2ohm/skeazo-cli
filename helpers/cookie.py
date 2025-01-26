# -*- coding:utf-8 -*-

import logging

import os
import yaml

import helpers.documents

logger = logging.getLogger(__name__)

# Cookie
# A cookie (file with yaml formatted data) is stored with each document

TITLE = "title"
AUTHOR = "author"
PUBLICATION = "date_of_publication"
SOURCE_NAME = "source_name"
SOURCE_URI = "source_uri"

class Cookie:
    def __init__(self, document_id):
        self.document_id = document_id
        self.cookie_path = helpers.documents.get_document_cookie_path(document_id)
        self.content = {}

    def __enter__(self):
        if os.path.isfile(self.cookie_path):
            self.content = yaml.safe_load(open(self.cookie_path, 'r'))
        else:
            self.content = {}

        return self.content
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.content:
            with open(self.cookie_path, 'w') as f:
                yaml.dump(self.content, f)