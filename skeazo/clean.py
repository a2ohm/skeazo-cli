#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging

import re
import os
import helpers.documents

CHAR_NBSP = ' '

logger = logging.getLogger(__name__)

def clean(args):
    document_id = args.id
    document_raw_md_path = helpers.documents.get_document_raw_md_path(document_id)
    document_edited_md_path = helpers.documents.get_document_edited_md_path(document_id)
    document_cleaned_md_path = helpers.documents.get_document_cleaned_md_path(document_id)

    # Create the cleaned file from (by order of priority)
    # - itself
    # - the edited file
    # - the raw file

    if args.force == 'from-raw':
        if os.path.isfile(document_raw_md_path):
            logger.info('Clean document from raw version. (forced)')
            in_filepath = document_raw_md_path
        else:
            logger.error("Raw markdown file not found.")
            logger.error(f"Run ./skeazo-cli.py convert {document_id}")
            return
    elif args.force == 'from-edited':
        if os.path.isfile(document_edited_md_path):
            logger.info('Clean document from edited version (forced).')
            in_filepath = document_edited_md_path
        else:
            logger.error("Edited markdown file not found.")
            logger.error(f"Run ./skeazo-cli.py edit {document_id}")
            return
    elif os.path.isfile(document_cleaned_md_path):
        logger.info('Clean document from cleaned version of itself.')
        in_filepath = document_cleaned_md_path
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
    
    with open(in_filepath, 'r', encoding='utf-8') as file_in:
        with open(document_cleaned_md_path, 'w', encoding='utf-8') as file_out:
            in_header = False

            for line in file_in.readlines():
                # Header is not cleaned
                if line == "---\n":
                    in_header = not in_header
                    file_out.write(line)
                elif in_header:
                    file_out.write(line)
                else:
                    file_out.write(do_cleaning(line))

def do_cleaning(line):
    # Strip leading and trailling spaces
    line = line[:-1].strip()

    # Set non breakable space before : ":;?!"
    pattern_punctution = re.compile(r"\b\s?(?P<punctuation>[:;?!])")
    line = pattern_punctution.sub(f"{CHAR_NBSP}\g<punctuation>", line)

    return f"{line}\n"