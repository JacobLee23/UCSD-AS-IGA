"""
A simple API wrapper and web scraper for the UCSD Associated Students (AS) instructor grade archive.
"""

from .scraper import GradeArchive
from .scraper import Parser


def main() -> None:
    parser = Parser(prog="asiga", description=__doc__, epilog="Go Tritons!")
    archive = parser.grade_archive

    print(archive.dataframe.to_string())
