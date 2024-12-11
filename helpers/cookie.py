# -*- coding:utf-8 -*-

import logging

import os
import yaml

import helpers.documents

logger = logging.getLogger(__name__)

# Cookie
# A cookie (.skeazo file with yaml formatted data) is stored with each document

class Cookie:
    TITLE = "title"
    AUTHOR = "author"
    PUBLICATION = "date_of_publication"
    SOURCE_NAME = "source_name"
    SOURCE_URI = "source_uri"

    def __init__(self, document_id):
        self.document_id = document_id
        self.cookie_path = os.path.join(helpers.documents.DOCUMENTS_ROOT_PATH, document_id, '.skeazo')
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