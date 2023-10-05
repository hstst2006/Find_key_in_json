#!/bin/python3

import argparse, json, sys

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("keys", type=str, nargs='*', help="One or more keys to look for")
    return parser

# Check if the filename ends in .json
def check_file_type(filename):
    if ".json" in filename:
        return True
    else:
        return False

# Recursively find all keys in the object
def dig_for_key(json_object, key_to_find):
    for key in json_object.keys():
        if str(key) == str(key_to_find):
            return True
        if isinstance(json_object[key], dict):
            return dig_for_key(json_object[key], key_to_find)

# Open file and gather list of matching keys
def process_file(filename, keys):
    file = open(filename, "r")
    json_object = json.load(file)
    keys_found = []
    # Look for keys
    for key in keys:
        if dig_for_key(json_object, key):
            keys_found.append(key)
    return keys_found

def main():
    
    parser = init_parser()
    args = parser.parse_args()

    # Check if there are keys to look for
    if len(args.keys) < 1:
        print("Missing argument: There are no keys to look for!")
        parser.print_help()
        exit(1)
    else:
        # Loop through stdin for filenames
        print("Pipe filenames to this script like so echo <filename> <filename2> <...> | ./find_key_in_json.py <key>.\nIf no filenames were supplied, type them manually here:\n>", end =" ")
        for filename in sys.stdin:
            filename = filename.strip()
            keys_found = []
            if check_file_type(filename):
                keys_found = process_file(filename, args.keys)
            else:
                print(f"{filename} is not .json!")

        # Print the filename, number of keys found and the list of keys found
            if len(keys_found) > 0:
                print(f"{filename : <50} {f'found {len(keys_found)}/{len(args.keys)} keys:' : ^20} {keys_found}")

if __name__ == "__main__":
    main()
