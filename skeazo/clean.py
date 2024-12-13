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
    document_cleaned_md_path = helpers.documents.get_document_cleaned_md_path(document_id)

    logging.debug("Clean document {}".format(document_id))

    if os.path.isfile(document_cleaned_md_path):
        # If a cleaned file already exist, cleaning rules are applied on it
        with open(document_cleaned_md_path, 'r', encoding='utf-8') as file_in:
            document = file_in.readlines()
    elif os.path.isfile(document_raw_md_path):
        with open(document_raw_md_path, 'r', encoding='utf-8') as file_in:
            document = file_in.readlines()
    else:
        logging.error("Mardown file not found.")
        logging.error(f"Run ./skeazo-cli.py convert {document_id}")
        return

    with open(document_cleaned_md_path, 'w', encoding='utf-8') as file_out:
        in_header = False

        for line in document:
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