import argparse
import pkg_resources

from .scraper import GradeArchive


VERSION = pkg_resources.get_distribution("ucsdasone").version


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} {VERSION}"
    )
    parser.add_argument("-q", "--quarter", type=str)
    parser.add_argument("-y", "--year", type=int)
    parser.add_argument("-i", "--instructor", type=str)
    parser.add_argument("-s", "--subject", type=str)
    parser.add_argument("-c", "--code", type=str)

    return parser


def main() -> None:
    parser = _parser()
    args = parser.parse_args()

    dataframe = GradeArchive(
        quarter=args.quarter,
        year=args.year,
        instructor=args.instructor,
        subject=args.subject,
        code=args.code
    )

    print(dataframe)
