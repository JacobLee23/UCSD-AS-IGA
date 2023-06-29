"""
A simple API wrapper and web scraper for the UCSD Associated Students (AS) instructor grade archive.
"""

import _scraper
from ._scraper import GradeArchive


def main() -> None:
    parser = _scraper.Parser(prog="asiga", description=__doc__, epilog="Go Tritons!")
    archive = parser.grade_archive

    print(archive.dataframe.to_string())
