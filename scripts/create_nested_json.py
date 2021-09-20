import argparse
import json
import sys


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("a", nargs="*")
    args, unknown = parser.parse_known_args()
    return args


def make_nested_json(sample_input, *args):
    result = {}
    _len = len(args)
    keys = sample_input[0].keys()
    # other keys
    other = {x for x in keys if x not in {*args}}  # set in better for searching
    for row in sample_input:
        cur = result
        for arg_i in range(_len):
            arg = args[arg_i]
            cur = cur.setdefault(row[arg], {} if arg_i != _len - 1 else [])
        cur.append({key: row[key] for key in other})
    return result


if __name__ == "__main__":
    file_content = data = sys.stdin.read()
    params = parse_arguments()
    print(make_nested_json(json.loads(file_content), *params.a))
