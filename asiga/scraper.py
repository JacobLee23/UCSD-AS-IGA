"""
"""

import collections
import datetime
import re
import typing

import pandas as pd
import requests


ADDRESS = "https://as.ucsd.edu/Home/InstructorGradeArchive"


MIN_YEAR = 15
MAX_YEAR = int(datetime.datetime.today().strftime("%y"))


def _validate_quarter(quarter: str) -> str:
    """
    :param quarter:
    :return:
    """
    values = ("FA", "WI", "SP")
    quarter = quarter.strip().upper()

    if quarter in values:
        return quarter

    return ""


def _validate_year(year: int) -> str:
    """
    :param year:
    :return:
    """
    if MIN_YEAR <= year <= MAX_YEAR:
        return str(year)

    return ""


def _validate_subject(subject: str) -> str:
    """
    :param subject:
    :return:
    """
    regex = re.compile(r"^[A-Z]{3,4}$")
    subject = subject.strip().upper()

    if regex.search(subject) is not None:
        return subject

    return ""


def _validate_code(code: str) -> str:
    """
    :param code:
    :return:
    """
    regex = re.compile(r"^\d{1,3}[A-Z]{0,2}$")
    code = code.strip().upper()

    if regex.search(code) is not None:
        return code

    return ""


def grade_archive(
    quarter: typing.Optional[str] = None,
    year: typing.Optional[int] = None,
    instructor: typing.Optional[str] = None,
    subject: typing.Optional[str] = None,
    code: typing.Optional[str] = None
) -> pd.DataFrame:
    """
    :param quarter:
    :param year:
    :param instructor:
    :param subject:
    :param code:
    :return:
    """
    form_data = collections.defaultdict()

    form_data["quarter"] = "" if quarter is None else _validate_quarter(quarter)
    form_data["year"] = "" if year is None else _validate_year(year)
    form_data["instructor"] = "" if instructor is None else instructor
    form_data["subject"] = "" if subject is None else _validate_subject(subject)
    form_data["courseNumber"] = "" if code is None else _validate_code(code)

    with requests.post(ADDRESS, form_data) as response:
        try:
            dfs = pd.read_html(response.text)
        except ValueError:
            return pd.DataFrame()

    assert len(dfs) == 1
    dataframe = dfs[0]

    columns = ["A", "B", "C", "D", "F", "W", "P", "NP"]
    dataframe[columns] = dataframe[columns].applymap(lambda x: float(x.strip("%")))

    return dataframe
