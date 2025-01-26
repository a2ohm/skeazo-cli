#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import re
import os
import datetime
import helpers.documents

CHAR_NBSP = ' '

logger = logging.getLogger(__name__)

def clean(args):
    document_id = args.id
    document_raw_md_path = helpers.documents.get_document_raw_md_path(document_id)
    document_edited_md_path = helpers.documents.get_document_edited_md_path(document_id)
    document_tmp_md_path = helpers.documents.get_document_tmp_md_path(document_id)
    document_logfile_path = helpers.documents.get_document_logfile_path(document_id)

    # Create the cleaned file from (by order of priority)
    # - the edited file
    # - the raw file

    if hasattr(args, 'force') and args.force == 'from-raw':
        if os.path.isfile(document_raw_md_path):
            logger.info('Clean document from raw version. (forced)')
            in_filepath = document_raw_md_path
        else:
            logger.error("Raw markdown file not found.")
            logger.error(f"Run ./skeazo-cli.py convert {document_id}")
            return
    elif os.path.isfile(document_edited_md_path):
        logger.info('Clean document from edited version.')
        in_filepath = document_edited_md_path
    elif os.path.isfile(document_raw_md_path):
        logger.info('Clean document from raw version.')
        in_filepath = document_raw_md_path
    else:
        logging.error("Mardown file not found.")
        logging.error(f"Run ./skeazo-cli.py convert {document_id}")
        return
    
    # Do cleaning line by line and save changes in the temporary file
    with open(in_filepath, 'r', encoding='utf-8') as file_in:
        with open(document_tmp_md_path, 'w', encoding='utf-8') as file_out:
            for line in file_in.readlines():
                file_out.write(do_cleaning(line))
    
    # Swap the temporary file with the edited file
    os.replace(document_tmp_md_path, document_edited_md_path)

    # Log cleaning
    with open(document_logfile_path, 'a', encoding='utf-8') as f:
        f.write(f"- ({datetime.datetime.now():%Y-%m-%d}) Nettoyage automatique par Skeazo\n")

def do_cleaning(line):
    # Strip leading and trailling spaces
    line = line[:-1].strip()

    # Set non breakable space before : ":;?!»"
    pattern_punctuation = re.compile(r"\b\s?(?P<punctuation>[:;?!»])")
    line = pattern_punctuation.sub(f"{CHAR_NBSP}\g<punctuation>", line)

    # Set non breakable space after : "«"
    pattern_punctuation = re.compile(r"(?P<punctuation>[«])\s?\b")
    line = pattern_punctuation.sub(f"\g<punctuation>{CHAR_NBSP}", line)

    # Add missing space after : "."
    pattern_punctuation = re.compile(r"\b(?P<punctuation>[.])\b")
    line = pattern_punctuation.sub(f"\g<punctuation> ", line)

    return f"{line}\n"