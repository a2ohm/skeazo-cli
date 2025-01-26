#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging
import argparse

import skeazo.download
import skeazo.convert
import skeazo.clean
import skeazo.edit
import skeazo.list

logging.basicConfig(level=logging.DEBUG)

# Parse arguments
parser = argparse.ArgumentParser(description="Get and clean documents for the Neomignes project")
subparsers = parser.add_subparsers()

# Create the parser for the 'get' command
def do_get(args):
    """Get a document: download it from an URL, convert it into markdown and clean it
    """
    args = skeazo.download.download(args)

    if args:
        skeazo.convert.convert(args)
        skeazo.clean.clean(args)

parser_get = subparsers.add_parser('get', help="Get a document: download it from an URL, convert it into markdown and clean it")
parser_get.add_argument('url', help="Document url")
parser_get.set_defaults(func=do_get)

# Create the parser for the 'download' command
parser_download = subparsers.add_parser('download', help="Download a document")
parser_download.add_argument('url', help="Document url")
parser_download.set_defaults(func=skeazo.download.download)

# Create the parser for the 'convert' command
parser_html2md = subparsers.add_parser('convert', help="Convert a local html document into markdown")
parser_html2md.add_argument('id', help="Document id")
parser_html2md.set_defaults(func=skeazo.convert.convert)

# Create the parser for the 'clean' command
parser_clean = subparsers.add_parser('clean', help="Clean a markdown file")
parser_clean.add_argument('id', help="Document id")
parser_clean.add_argument('-f', '--force', choices = ['from-raw', 'from-edited'], help="Force document cleaning from a specific file")
parser_clean.set_defaults(func=skeazo.clean.clean)

# Create the parser for the 'edit' command
parser_edit = subparsers.add_parser('edit', help="Edit manually the markdown file")
parser_edit.add_argument('id', help="Document id")
parser_edit.set_defaults(func=skeazo.edit.edit)

# Create the parser for the 'list' command
parser_list = subparsers.add_parser('list', help="List documents")
#parser_list.add_argument('id', help="Document id")
parser_list.set_defaults(func=skeazo.list.list)

# Parse
args = parser.parse_args()

# Call the right module
args.func(args)