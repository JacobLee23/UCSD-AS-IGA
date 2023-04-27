"""
"""

import datetime
import pathlib
import re
import typing

import pandas as pd
import requests


MIN_YEAR = 15
MAX_YEAR = int(datetime.datetime.today().strftime("%y"))


class GradeArchive:
    """

    :param quarter:
    :param year:
    :param instructor:
    :param subject:
    :param code:
    """
    address = "https://as.ucsd.edu/Home/InstructorGradeArchive"

    quarter_values = ["FA", "WI", "SP"]
    subject_regex = re.compile(r"^[A-Z]{3,4}$")
    code_regex = re.compile(r"^\d{1,3}[A-Z]{0,2}$")

    def __init__(
        self,
        quarter: typing.Optional[str] = None,
        year: typing.Optional[int] = None,
        instructor: typing.Optional[str] = None,
        subject: typing.Optional[str] = None,
        code: typing.Optional[str] = None
    ):
        self.quarter = ""
        if isinstance(quarter, str) and quarter.upper() in self.quarter_values:
            self.quarter = quarter.upper()

        self.year = ""
        if isinstance(year, int):
            self.year = int(year)
            assert MIN_YEAR <= self.year <= MAX_YEAR

        self.instructor = ""
        if isinstance(instructor, str):
            self.instructor = instructor.strip()

        self.subject = ""
        if isinstance(subject, str):
            self.subject = subject.upper().strip()
            assert self.subject_regex.search(self.subject) is not None

        self.code = ""
        if isinstance(code, (str, int)):
            self.code = (str(code) if isinstance(code, int) else code.upper().strip())
            assert self.code_regex.search(self.code) is not None

        self.form_data = {
            "quarter": self.quarter,
            "year": str(self.year),
            "instructor": self.instructor,
            "subject": self.subject,
            "courseNumber": self.code
        }
        self.response = requests.post(self.address, self.form_data, timeout=100)

    def data(self) -> pd.DataFrame:
        """
        :return:
        """
        try:
            dfs = pd.read_html(self.response.text)
        except ValueError:
            return pd.DataFrame()

        assert len(dfs) == 1
        dataframe = dfs[0]

        columns = ["A", "B", "C", "D", "F", "W", "P", "NP"]
        dataframe[columns] = dataframe[columns].applymap(lambda x: float(x.strip("%")))

        return dataframe

    def export(self, path: typing.Union[str, pathlib.Path]) -> pathlib.Path:
        """

        :param path:
        :return:
        """
        path = pathlib.Path(path)
        dataframe = self.data()

        if path.suffix == ".csv":
            dataframe.to_csv(path)
        else:
            with open(path, "w", encoding="utf-8") as file:
                dataframe.to_string(file)

        return path
