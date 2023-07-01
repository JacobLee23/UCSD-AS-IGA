"""
"""

import argparse
import datetime
from importlib import metadata
import re
import typing

import pandas as pd
import requests


class GradeArchive:
    """
    .. py:attribute:: quarters

        A list of values to which :py:attr:`GradeArchive.quarter` can be set.

    .. py:attribute:: years

        A list of values to which :py:attr:`GradeArchive.year` can be set.

    :param quarter: See :py:attr:`GradeArchive.quarter`.
    :param year: See :py:attr:`GradeArchive.year`.
    :param instructor: See :py:attr:`GradeArchive.instructor`.
    :param subject: See :py:attr:`GradeArchive.subject`.
    :param code: See :py:attr:`GradeArchive.code`.
    """
    _url = "https://as.ucsd.edu/Home/InstructorGradeArchive"
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
    }
    _timeout = 100

    _fields: typing.List[str] = ["quarter", "year", "instructor", "subject", "code"]
    quarters: typing.List[str] = ["FA", "WI", "SP"]
    years: typing.List[int] = list(range(15, datetime.datetime.today().year))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self._fields:
                raise AttributeError(key)
            self.__setattr__(key, value)

    def __getitem__(self, key: str) -> typing.Optional[typing.Union[str, int]]:
        return self.__getattribute__(key)

    @property
    def quarter(self) -> typing.Optional[str]:
        """
        Filters results to a specific quarter.

        .. note::

            See :py:attr:`GradeArchive.quarters` for property options.
        """
        return self._quarter

    @quarter.setter
    def quarter(self, value: typing.Optional[str]) -> None:
        """
        :param value:
        """
        if isinstance(value, str):
            quarter = value.strip().upper()
            self._quarter = quarter if quarter in self.quarters else None
        else:
            self._quarter = None

    @property
    def year(self) -> typing.Optional[int]:
        """
        Filters results to a specific year.

        .. note::

            See :py:attr:`GradeArchive.years` for property options.
        """
        return self._year

    @year.setter
    def year(self, value: typing.Optional[int]) -> None:
        """
        :param value:
        """
        if isinstance(value, int):
            self._year = value if value in self.years else None
        else:
            self._year = None

    @property
    def instructor(self) -> typing.Optional[str]:
        """
        Filters results to classes taught by a specific instructor.

        .. note::

            Format: `{{Last Name}}, {{First Name}}`.
        """
        return self._instructor

    @instructor.setter
    def instructor(self, value: typing.Optional[str]) -> None:
        """
        :param value:
        """
        if isinstance(value, str):
            self._instructor = value
        else:
            self._instructor = None

    @property
    def subject(self) -> typing.Optional[str]:
        """
        Filters results to classes taught in a specific department.
        """
        return self._subject

    @subject.setter
    def subject(self, value: typing.Optional[str]) -> None:
        """
        :param value:
        """
        regex = re.compile(r"^[A-Z]{3,4}$")
        if isinstance(value, str):
            subject = value.strip().upper()
            self._subject = None if regex.search(subject) is None else subject
        else:
            self._subject = None

    @property
    def code(self) -> typing.Optional[str]:
        """
        Filters results to a specific course number.
        """
        return self._code

    @code.setter
    def code(self, value: typing.Optional[str]) -> None:
        """
        :param value:
        """
        regex = re.compile(r"^\d{1,3}[A-Z]{0,2}$")
        if isinstance(value, str):
            code = value.strip().upper()
            self._code = None if regex.search(code) is None else code
        else:
            self._code = None

    @property
    def dataframe(self) -> pd.DataFrame:
        """
        """
        data = {
            "quarter": "" if self.quarter is None else self.quarter,
            "year": "" if self.year is None else str(self.year),
            "instructor": "" if self.instructor is None else self.instructor,
            "subject": "" if self.subject is None else self.subject,
            "courseNumber": "" if self.code is None else self.code
        }
        with requests.post(
            self._url, data=data, headers=self._headers, timeout=self._timeout
        ) as response:
            try:
                dataframe = pd.read_html(response.text)[0]
            except ValueError:
                return pd.DataFrame({})

        columns = ["A", "B", "C", "D", "F", "W", "P", "NP"]
        dataframe[columns] = dataframe[columns].applymap(lambda x: float(x.strip("%")))

        return dataframe


class Parser(argparse.ArgumentParser):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument(
            "-v", "--version", action="version",
            version=f"%(prog)s {metadata.version('ucsdasone')}"
        )
        self.add_argument("-q", "--quarter", type=str, help=GradeArchive.quarter.__doc__)
        self.add_argument("-y", "--year", type=int, help=GradeArchive.year.__doc__)
        self.add_argument("-i", "--instructor", type=str, help=GradeArchive.instructor.__doc__)
        self.add_argument("-s", "--subject", type=str, help=GradeArchive.subject.__doc__)
        self.add_argument("-c", "--code", type=str, help=GradeArchive.code.__doc__)

    @property
    def grade_archive(self) -> GradeArchive:
        """
        """
        return GradeArchive(**self.parse_args().__dict__)
