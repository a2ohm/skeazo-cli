#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import os
import datetime
import subprocess
import helpers.documents

logger = logging.getLogger(__name__)

def edit(args):
    document_id = args.id
    document_raw_md_path = helpers.documents.get_document_raw_md_path(document_id)
    document_edited_md_path = helpers.documents.get_document_edited_md_path(document_id)
    document_logfile_path = helpers.documents.get_document_logfile_path(document_id)

    logging.debug("Edit document {}".format(document_id))

    if not os.path.isfile(document_edited_md_path):
        # The edited file does not exist
        # Create it from (by order of priority)
        # - raw markdown file
        if os.path.isfile(document_raw_md_path):
            in_filepath = document_raw_md_path
        else:
            logger.error("Markdown file not found.")
            logger.error(f"Run ./skeazo convert {document_id}")
            return
        
        with open(in_filepath, 'r', encoding='utf-8') as f_in:
            with open(document_edited_md_path, 'w', encoding='utf-8') as f_out:
                for line in f_in.readlines():
                    f_out.write(line)
        
    # Open edited version file of the markdown file
    subprocess.call(('xdg-open', document_edited_md_path))

    # Log modifications
    print("Quelles modifications avez-vous faites ?")

    with open(document_logfile_path, 'a', encoding='utf-8') as f:
        while True:
            log = input('> ')
            if log:
                f.write(f"- ({datetime.datetime.now():%Y-%m-%d}) {log}\n")
            else:
                break