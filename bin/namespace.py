import argparse


class InputNamespace(argparse.Namespace):
    filepath: str
    method: str
    status: str     # can be range
    start: int      # timestamp
    end: int        # timestamp
    top: int