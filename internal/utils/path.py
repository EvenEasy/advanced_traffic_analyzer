import argparse
import os


def valid_path(path):
    return os.path.abspath(os.path.expanduser(path))

def validate_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"{path} is not a valid file.")
    return path