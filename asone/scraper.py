"""
"""

import datetime
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

    quarter_values = {
        "all": "", "fall": "FA", "winter": "WI", "spring": "SP"
    }
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
        if isinstance(quarter, str):
            self.quarter = self.quarter_values[quarter.lower().strip()]
        else:
            self.quarter = ""

        if isinstance(year, int):
            self.year = int(year)
            assert MIN_YEAR <= self.year <= MAX_YEAR
            self.year = str(year)
        else:
            self.year = ""

        if isinstance(instructor, str):
            self.instructor = instructor.strip()
        else:
            self.instructor = ""

        if isinstance(subject, str):
            self.subject = subject.upper().strip()
            assert self.subject_regex.search(self.subject) is not None
        else:
            self.subject = ""

        if isinstance(code, (str, int)):
            self.code = (str(code) if isinstance(code, int) else code.upper().strip())
            assert self.code_regex.search(self.code) is not None
        else:
            self.code = ""

        self.form_data = {
            "quarter": self.quarter,
            "year": str(self.year),
            "instructor": self.instructor,
            "subject": self.subject,
            "courseNumber": self.code
        }
        
    def request(self) -> requests.Response:
        """
        :return:
        """
        return requests.post(self.address, self.form_data)
    
    def data(self) -> pd.DataFrame:
        """
        :return:
        """
        with self.request() as response:
            try:
                dfs = pd.read_html(response.content)
            except ValueError:
                return pd.DataFrame()
            
        assert len(dfs) == 1
        df = dfs[0]

        columns = ["A", "B", "C", "D", "F", "W", "P", "NP"]
        df[columns] = df[columns].applymap(lambda x: float(x.strip("%")))

        return df
