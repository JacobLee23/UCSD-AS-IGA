import argparse
from importlib import metadata

from .scraper import GradeArchive


NAME = metadata.metadata("ucsdasone")["name"]
VERSION = metadata.version("ucsdasone")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asiga",
        description="A simple API wrapper and web scraper for the UCSD Associated Students (AS) instructor grade archive.",
        epilog="Go Tritons!"
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"$(prog) {VERSION}"
    )
    parser.add_argument(
        "-q", "--quarter", type=str,
        help="filter results to the fall ('FA'), winter ('WI'), or spring ('SP')"
    )
    parser.add_argument(
        "-y", "--year", type=int,
        help=r"filter results to a specific year (r'^\d\d$')."
    )
    parser.add_argument(
        "-i", "--instructor", type=str,
        help="filter results to classes taught by a specific instructor (f'{last_name}, {first_name}')"
    )
    parser.add_argument(
        "-s", "--subject", type=str,
        help="filter results to classes in a specific department (r'^[A-Z]{3,4}$')"
    )
    parser.add_argument(
        "-c", "--code", type=str,
        help=r"filter results to a specific course number (r'^[0-9]{1,3}[A-Z]{0,2}$')"
    )

    return parser


def main() -> None:
    parser = _parser()
    args = parser.parse_args()

    archive = GradeArchive(
        quarter=args.quarter,
        year=args.year,
        instructor=args.instructor,
        subject=args.subject,
        code=args.code
    )
    dataframe = archive.data()

    print(dataframe.to_string())
