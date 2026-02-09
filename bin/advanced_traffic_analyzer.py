import os
import sys
import argparse

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from internal.entity import FilterOpt, ALLOWED_METHODS
from internal.anazyler import AdvancedTrafficAnalyzer
from internal.utils.filter import get_status_code_range
from internal.utils.path import validate_file
from internal.view import ViewReport
from bin.namespace import InputNamespace


def build_report(inp: InputNamespace):
    # Validate inputs
    if inp.top and inp.top <= 0:
        print("Error: --top must be a positive integer")
        return
    
    if inp.start and inp.end and inp.start > inp.end:
        print("Error: --start timestamp must be less than or equal to --end")
        return
    
    # Build filter
    start_status, end_status = get_status_code_range(inp.status)
    fltr = FilterOpt(inp.top, inp.start, inp.end, inp.method, start_status, end_status)

    # Build analyzer and ViewModel
    analyzer = AdvancedTrafficAnalyzer(fltr)
    view = ViewReport()

    # Get report and out data
    try:
        report = analyzer.get_report(inp.filepath)
        if report.total_requests == 0:
            print("Warning: No matching requests found with the given filters")
    except Exception as e:
        print(f"Error: {e}")
        return
    try:
        view.show_report(report, analyzer.filter)
    except Exception as e:
        print(f"Error showing report: {e}")


def main():
    parser = argparse.ArgumentParser("ADVANCED TRAFFIC ANALYZER")

    sub = parser.add_subparsers(dest="command", required=True)

    # build
    p1 = sub.add_parser("parse", help="Parse access log")
    p1.add_argument('-f', '--filepath',type=validate_file, required=True)
    p1.add_argument("--method", choices=ALLOWED_METHODS)
    p1.add_argument("--status", type=str)
    p1.add_argument("--start", type=int)
    p1.add_argument("--end", type=int)
    p1.add_argument("--top", type=int, default=3)

    # start building
    args = parser.parse_args(namespace=InputNamespace())
    build_report(args)

if __name__ == '__main__':
    main()
