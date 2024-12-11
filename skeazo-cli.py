#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging
import argparse

import skeazo.download
import skeazo.convert
import skeazo.clean

logging.basicConfig(level=logging.DEBUG)

# Parse arguments
parser = argparse.ArgumentParser(description="Get and clean documents for the Neomignes project")
subparsers = parser.add_subparsers()

# Create the parser for the 'download' command
parser_download = subparsers.add_parser('download', help="Download a document")
parser_download.add_argument('url', help="Document url")
parser_download.set_defaults(func=skeazo.download.download)

# Create the parser for the 'html2md' command
parser_html2md = subparsers.add_parser('convert', help="Convert a local html document into markdown")
parser_html2md.add_argument('id', help="Document id")
parser_html2md.set_defaults(func=skeazo.convert.convert)

# Create the parser for the 'clean' command
parser_clean = subparsers.add_parser('clean', help="Clean a markdown file")
parser_clean.add_argument('id', help="Document id")
parser_clean.set_defaults(func=skeazo.clean.clean)

# Parse
args = parser.parse_args()

# Call the right module
args.func(args)