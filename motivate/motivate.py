#!/usr/bin/env python3

import json
import os
import random
import argparse
import jsonschema

data_file_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "quote": {"type": "string"},
                    "author": {"type": "string"}
                },
                "required": ["quote", "author"]
            }
        }
    }
}

def getlink(file):
    if os.path.islink(file):
        path = os.path.dirname(os.readlink(file))
    else:
        path = os.path.dirname(file)

    return os.path.dirname(path)


def quote():
    abspath = getlink(__file__)

    if os.name == 'nt':
        data_dir = os.path.join(abspath, 'motivate', 'data')
    else:
        data_dir = os.path.join('/opt', 'motivate', 'data')

    try:
        data_files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))] # get file names as list
    except FileNotFoundError:
        print("Can't find the data folder. You probably haven't run 'install.sh' yet.")
        exit(1)


    filename = os.path.join(data_dir, data_files[random.randrange(len(data_files))]) # pick a random file and construct a path
    
    with open(filename) as json_data:
        try:
            quotes = json.load(json_data)
            jsonschema.validate(instance=quotes, schema=data_file_schema)
        except ValueError as value_err:
            print("ValueError in file {0}\n{1}".format(filename, value_err))
            exit(1)
        except jsonschema.exceptions.ValidationError as validation_err:
            print("ValidationError in file {0}\n{1}".format(filename, validation_err.message))
            exit(1)

        quote = quotes["data"][random.randrange(len(quotes["data"]))]
        if (os.name == "nt") or args.nocolor:
            print("\"{0}\"\n\t\t{1}".format(quote["quote"], quote["author"]))
        else:
            print("\033[1;36m\"{0}\"\n\t\t\033[1;35m--{1}".format(quote["quote"], quote["author"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A simple script to print random motivational quotes.')
    parser.add_argument('--no-colors', dest='nocolor', default=False, action='store_true', help='Argument to disable colored output. Disabled by default.')
    args = parser.parse_args()

    quote()
