# -*- coding:utf-8 -*-

import logging

import os
from gi.repository import GLib

import hashlib

logger = logging.getLogger(__name__)

# Config
DOCUMENTS_ROOT_PATH = os.path.join(GLib.get_user_data_dir(), 'skeazo', 'documents')
THEKE_CACHE_PATH = os.path.join(GLib.get_user_data_dir(), 'theke', 'cache')
OUT_PATH = './out'

ID_SIZE = 8-1

# Helpers
def get_document_id_from_url(document_url):
    """A document id = ID_SIZE first characters of url's md5 
    """
    return hashlib.md5(document_url.encode()).hexdigest()[0:ID_SIZE]

def get_document_directory_path(document_id):
    return os.path.join(DOCUMENTS_ROOT_PATH, document_id)

def get_document_raw_html_path(document_id):
    return os.path.join(DOCUMENTS_ROOT_PATH, document_id, "{}_raw.html".format(document_id))

def get_document_raw_md_path(document_id):
    return os.path.join(DOCUMENTS_ROOT_PATH, document_id, "{}_raw.md".format(document_id))

def get_document_edited_md_path(document_id):
    return os.path.join(DOCUMENTS_ROOT_PATH, document_id, "{}_edited.md".format(document_id))

def get_document_cleaned_md_path(document_id):
    return os.path.join(DOCUMENTS_ROOT_PATH, document_id, "{}_cleaned.md".format(document_id))

def get_document_logfile_path(document_id):
    return os.path.join(DOCUMENTS_ROOT_PATH, document_id, "{}_logfile.md".format(document_id))