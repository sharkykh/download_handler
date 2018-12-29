# coding=utf-8
from __future__ import print_function

""" Simple post-download processor for torrents """
__author__ = 'sharkykh'
__version__ = '1.0.1'

# Recommended:
#   After configuring as needed, run the file with the `pyw` extension in order to avoid opening a console window.

# Usage: download_handler.py [-h] path label
#
# positional arguments:
#   path        full path to downloaded folder
#   label       torrent label
#
# optional arguments:
#   -h, --help  show this help message and exit

import argparse
import json
import os
import subprocess
import sys

import requests
import urllib3

from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

if sys.version_info[0] == 3:
    string_types = str,
else:
    string_types = basestring,


SUPPORTED_LIBRARY_MANAGERS = {
    'm': 'Medusa',  # Set LIBRARY_MANAGER_TYPE to 'm' if you use Medusa
    'sc': 'SickChill'  # Set LIBRARY_MANAGER_TYPE to 'sc' if you use SickChill
    'sr': 'SickRage'  # Set LIBRARY_MANAGER_TYPE to 'sr' if you use SickRage
}

# Configuration:
LIBRARY_MANAGER_TYPE = 'm'  # Choose from SUPPORTED_LIBRARY_MANAGERS (left column)
LIBRARY_MANAGER_URL = 'http://localhost:8081'  # Set this to your TV Library Manager URL
LIBRARY_MANAGER_API_KEY = 'CHANGEME'  # Set this to your TV Library Manager API key
PROCESS_LABELS = [  # Only torrents with these labels will get sent to your TV Library Manager for processing
    'tv',
]
POST_PROCESS_OPTIONS = {
    # How should valid post-processed files be handled
    # Allowed: 'copy' / 'move' / 'hardlink' / 'symlink' / 'symlink_reversed'
    'process_method': 'copy',
    # The type of post-process being requested
    # Allowed: 'auto' / 'manual'
    'type': 'auto',
    # Mark download as failed.
    # Allowed: 0 / 1  [= Off / On]
    'failed': 0,
    # Waits for the current processing queue item to finish and returns result of this request.
    # Allowed: 0 / 1  [= Off / On]
    'force_next': 0,
    # Force already post-processed files to be post-processed again
    # Allowed: 0 / 1  [= Off / On]
    'force_replace': 0,
    # Replace the file even if it exists in a higher quality
    # Allowed: 0 / 1  [= Off / On]
    'is_priority': 0,
    # Returns the result of the post-process
    # Allowed: 0 / 1  [= Off / On]
    'return_data': 0,
    # Delete processed files and folders
    # Allowed: 0 / 1  [= Off / On]
    'delete': 0
}


class TvLibraryManagerApi(object):
    def __init__(self):
        self.manager = SUPPORTED_LIBRARY_MANAGERS[LIBRARY_MANAGER_TYPE]
        self.url = '{0}/api/{1}/'.format(LIBRARY_MANAGER_URL, LIBRARY_MANAGER_API_KEY)
        
        process_methods = ['copy', 'move', 'hardlink', 'symlink']
        if LIBRARY_MANAGER_TYPE in ('sc', 'sr'):
            process_methods.append('symlink_reversed')

        self.supported_commands = {
            'postprocess': {
                'path': [],
                'process_method': process_methods,
                'type': ['auto', 'manual'],
                'failed': [0, 1],
                'force_next': [0, 1],
                'force_replace': [0, 1],
                'is_priority': [0, 1],
                'return_data': [0, 1],
                'delete': [0, 1]
            }
        }

    def call(self, cmd, opts):
        cmd = cmd.lower()
        if cmd not in self.supported_commands.keys():
            raise NotImplementedError()

        payload = {
            'cmd': cmd
        }

        for key, value in opts.items():
            key = key.lower()
            value = value.lower() if isinstance(value, string_types) else value

            if key not in self.supported_commands[cmd]:
                print('unsupported option: "{k}" for cmd: "{c}"'.format(k=key, c=cmd))
                return False

            if self.supported_commands[cmd][key] and value not in self.supported_commands[cmd][key]:
                print('incorrect value : "{v}" for option: "{k}" for cmd: "{c}"'.format(v=value,
                                                                                        k=key,
                                                                                        c=cmd))
                return False

            payload[key] = value

        try:
            r = requests.get(self.url, params=payload, verify=False)
            r.raise_for_status()
        except Exception as e:
            print('Error calling {0} API: {1!r}'.format(self.manager, e))
            return False

        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='full path to downloaded folder')
    parser.add_argument('--label', help='torrent label', required=True)
    args = parser.parse_args()

    console = sys.stdin.isatty()
    if console:
        print('Path:\t' + args.path)
        print('Label:\t' + args.label)

    if args.label.lower() in map(str.lower, PROCESS_LABELS):
        api = TvLibraryManagerApi()
        print('Sending to ' + api.manager)
        options = POST_PROCESS_OPTIONS
        options.update({'path': args.path})
        api_result = api.call('postprocess', options)

if __name__ == '__main__':
    main()
