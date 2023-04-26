import argparse
from importlib import metadata
import pathlib

from .scraper import GradeArchive


NAME = metadata.metadata("ucsdasone")["name"]
VERSION = metadata.version("ucsdasone")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{NAME} {VERSION}"
    )
    parser.add_argument("-q", "--quarter", type=str)
    parser.add_argument("-y", "--year", type=int)
    parser.add_argument("-i", "--instructor", type=str)
    parser.add_argument("-s", "--subject", type=str)
    parser.add_argument("-c", "--code", type=str)
    parser.add_argument("-o", "--output", type=str)

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

    if args.output:
        archive.export(args.output)

    print(dataframe.to_string())
