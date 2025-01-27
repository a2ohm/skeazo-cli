# -*- coding:utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import sqlite3

from gi.repository import GLib
from collections import namedtuple

import helpers.cookie
import helpers.documents

DOCUMENT_ROOT_PATH = os.path.join(GLib.get_user_data_dir(), 'skeazo', 'documents')
INDEX_PATH = os.path.join(GLib.get_user_data_dir(), 'skeazo', 'index.db')

DocumentMainData = namedtuple('documentMainData', ['id', 'title', 'author', 'date_of_publication', 'source_name', 'source_uri'])

class Index:
    """Helper to use the index of a Theke repository
    """

    def __init__(self, path = INDEX_PATH):
        self.con = sqlite3.connect(path)

    def execute(self, sql, parameters = ()):
        """Execute a sql query
        """
        return self.con.execute(sql, parameters)
    
    def commit(self):
        """Commit last modifications of the index
        """
        self.con.commit()

    # GET
    def get_document_by_id(self, id):
        """Return a document given its id
        """

        rawDocumentData = self.con.execute("""SELECT id, title, author, date_of_publication, source_name, source_uri
            FROM documents
            WHERE id=?;""",
            (id,)).fetchone()

        return None if rawDocumentData is None else DocumentMainData._make(rawDocumentData)
    
    # LIST
    def list_all_documents(self, order = 'title'):
        """List all documents
        """
        
        rawDocumentsData = self.execute(f"""SELECT id, title, author, date_of_publication, source_name, source_uri
                FROM documents
                ORDER BY {order}""")

        for rawDocumentData in rawDocumentsData:
            yield DocumentMainData._make(rawDocumentData)
    
    # EDIT
    def add_document(self, id, metadata, doCommit = True):
        logger.debug(f"Index: add new document ({id} {metadata['title']})")

        self.execute("""INSERT INTO documents (id, title, author, date_of_publication, source_name, source_uri)
                    VALUES(?, ?, ?, ?, ?, ?);""",
                    (id,
                     metadata[helpers.cookie.TITLE],
                     metadata[helpers.cookie.AUTHOR],
                     metadata[helpers.cookie.PUBLICATION],
                     metadata[helpers.cookie.SOURCE_NAME],
                     metadata[helpers.cookie.SOURCE_URI],
                     ))
        
        if doCommit:
            self.commit()
    
    def update_document(self, id, metadata, doCommit = True):
        logger.debug(f"Index: update document ({id} {metadata.title})")

        self.execute_returning_id("""UPDATE documents
                SET title = ?,
                    author = ?,
                    date_of_publication = ?,
                    source_name = ?,
                    source_uri = ?
                WHERE id = ?;""",
            (metadata[helpers.cookie.TITLE],
             metadata[helpers.cookie.AUTHOR],
             metadata[helpers.cookie.PUBLICATION],
             metadata[helpers.cookie.SOURCE_NAME],
             metadata[helpers.cookie.SOURCE_URI],
             id))
            
        if doCommit:
            self.commit()

def init_index(path = INDEX_PATH):
    index = Index(path)

    # Crate the documents table
    logger.debug("Init the index...")

    index.execute("""CREATE TABLE IF NOT EXISTS documents (
        id text PRIMARY KEY,
        title text NOT NULL,
        author text NOT NULL,
        date_of_publication DATE NOT NULL,
        source_name text NOT NULL,
        source_uri text NOT NULL
        );""")

    # Index each document
    with os.scandir(helpers.documents.DOCUMENTS_ROOT_PATH) as it :
        for entry in it:
            if entry.is_dir():
                id = entry.name
                # Check if the document is already in the index
                documentData = index.get_document_by_id(id)
                
                with helpers.cookie.Cookie(id) as metadata:
                    if documentData is None:
                        # This is a new document
                        index.add_document(id, metadata, doCommit=False)
                    else:
                        # This document is already in the index
                        index.update_document(id, metadata)
    
    # Commit changes
    index.commit()