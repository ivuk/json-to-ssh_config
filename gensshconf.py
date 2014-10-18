#!/usr/bin/env python3

import argparse
from collections import OrderedDict
import json
import os


def list_files(input_dir):
    """
    Go through each file in the input_dir
    If it ends in a .conf suffix, add it to a set
    For each element in set open it with json.load()
    If it works, add it to a list
    If it fails, print a message and ignore the file
    Sort the final list, if there is an element called 'global.conf'
    make sure it's the last element in the list
    Return the final list
    """
    conf_files = {os.path.join(input_dir, files) for
                  files in os.listdir(input_dir)
                  if files.endswith('.conf')}

    conf_files_filtered = list()

    for files in conf_files:
        try:
            with open(files) as f:
                json.load(f)
        except ValueError as e:
            print("Got ValueError: {0}".format(e))
        else:
            conf_files_filtered.append(files)

    conf_files_filtered_sorted = sorted(conf_files_filtered)
    global_config_file = os.path.join(input_dir, 'global.conf')

    if global_config_file in conf_files_filtered_sorted:
        conf_files_filtered_sorted.remove(global_config_file)
        conf_files_filtered_sorted.append(global_config_file)

    return conf_files_filtered_sorted


def load_files(input_dir):
    """
    For each file gotten from list_files() function
    Create a dictionary with the name of the file and content as OrderedDict()
    Return the OrderedDict()
    """
    conf_data = OrderedDict()

    for conf_files in list_files(input_dir):
        with open(conf_files) as conf_file:
            conf_data[conf_files] = json.load(conf_file,
                                              object_pairs_hook=OrderedDict)

    return conf_data


def parse_files(input_dir, output_type):
    conf_files = load_files(input_dir)

    # If the output_type is file
    # Try to remove the existing FILE_NAME
    # I'm intentionally not using `with suppress`
    if output_type == 'file':
        try:
            os.remove(FILE_NAME)
        except OSError:
            pass

    for dict_file_key, dict_file in conf_files.items():
        out = list()
        default_values = set()

        for inner_key, inner_value in dict_file.items():
            if inner_key == "default":
                for elem in inner_value.items():
                    default_values.add('  {0} {1}'.format(elem[0], elem[1]))
            elif inner_key == "Host":
                if isinstance(inner_value, dict):
                    for elem in inner_value.items():
                        out.append('Host {0}'.format(elem[0]))
                        out.append('  HostName {0}'.format(elem[1]))
                        if default_values:
                            for elem in default_values:
                                out.append(elem)
                elif isinstance(inner_value, str):
                    out.append('Host {0}'.format(inner_value))
                    if default_values:
                        for elem in default_values:
                            out.append(elem)
            else:
                out.append('  {0} {1}'.format(inner_key, inner_value))

        if output_type == 'screen':
            print('# Content from {0}\n{1}'.format(dict_file_key,
                                                   '\n'.join(out)))
        elif output_type == 'file':
            with os.fdopen(os.open(
                    FILE_NAME, os.O_WRONLY | os.O_CREAT, 0o600), 'a') as f:
                f.write('# Content from {0}\n{1}\n'.format(dict_file_key,
                                                           '\n'.join(out)))


def do_it():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source-dir', dest='source_dir',
                        help='Set the source directory from which the files \
                        will be loaded', type=str, action='store',
                        default=os.path.expanduser('~') + '/.ssh/confs/')
    parser.add_argument('-o', '--output', dest='output', help='Set the \
                        output type', type=str, action='store',
                        default='screen')
    parser.add_argument('-f', '--file', dest='file_name', help='Set the file \
                        name of the output file', type=str, action='store',
                        default=os.path.join(os.path.dirname(
                            os.path.abspath(__file__)), 'outfile-example'))

    args = parser.parse_args()

    if args.output == 'file' and args.file_name:
        global FILE_NAME
        FILE_NAME = args.file_name

    if args.source_dir:
        parse_files(args.source_dir, args.output)

if __name__ == '__main__':
    do_it()
