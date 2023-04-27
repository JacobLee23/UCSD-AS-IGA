# UCSD Associated Students (AS) Instructor Grade Archive (IGA)

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/JacobLee23/UCSD-AS-IGA)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ucsdasiga)](https://pypi.org/project/ucsdasiga)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/JacobLee23/UCSD-AS-IGA)](https://github.com/JacobLee23/UCSD-AS-IGA/tags)
[![GitHub](https://img.shields.io/github/license/JacobLee23/UCSD-AS-IGA)](https://github.com/JacobLee23/UCSD-AS-IGA/blob/master/LICENSE)
![GitHub Repo stars](https://img.shields.io/github/stars/JacobLee23/UCSD-AS-IGA?style=social)

A simple API wrapper and web scraper for the UCSD Associated Students (AS) [instructor grade archive](https://as.ucsd.edu/Home/InstructorGradeArchive).
***

## Quickstart

### Python Usage

Start by importing the [`GradeArchive` class](https://github.com/JacobLee23/UCSD-AS-IGA/blob/master/asiga/scraper.py) from the `ucsdasiga` package:

```python
>>> from asiga import GradeArchive
```

`GradeArchive` class accepts 5 optional arguments:

| Parameter     | Type  | Description                                                                                             |
| :------------ | :---: | :------------------------------------------------------------------------------------------------------ |
| `quarter`     | `str` | Filter results to the fall (`"FA"`), winter (`"WI"`), or spring (`"SP"`).                               |
| `year`        | `int` | Filter results to a specific year (`r"^\d\d$"`).                                                        |
| `instructor`  | `str` | Filter results to classes taught by a specific instructor (`f"{last_name}, {first_name}"`). _[1]_       |
| `subject`     | `str` | Filter results to classes in a specific department (`r"^[A-Z]{3,4}$"`) (e.g., `"CSE"`, `"MCWP"`). _[2]_ |
| `code`        | `str` | Filter results to a specific course number (`r"^[0-9]{1,3}[A-Z]{0,2}$"`) (e.g., `"11"`, `"20"`).        |

- [1]: See the [UCSD website](https://hwsph.ucsd.edu/people/faculty/faculty-directory.html) for the faculty directory.
- [2]: See the [UCSD website](https://blink.ucsd.edu/instructors/courses/schedule-of-classes/subject-codes.html) for a comprehensive list of active department subject codes.

The following Python call generates the grade archive of all _CSE 11_ classes (regardless of quarter and the instructor who taught the class) that occurred during the 2021 academic year:

```python
>>> archive = GradeArchive(year=21, subject="CSE", code="11")
>>> archive.data()
  Subject  Course  Year Quarter                        Title               Instructor    GPA     A      B     C     D     F     W      P     NP
0     CSE      11    21      WI  Accel. Intro to Programming             Cao, Yingjun  3.284  37.9  22.80  4.67  1.92  2.19  6.04  14.50   6.31
1     CSE      11    21      SP  Accel. Intro to Programming  Miranda, Gregory Joseph  3.485  51.3   9.33  4.28  0.38  4.28  7.39  12.40  10.10
2     CSE      11    21      FA  Accel. Intro to Programming     Politz, Joseph Gibbs  3.484  68.4  18.20  2.61  3.39  4.43  1.56   0.78   0.52
3     CSE      11    21      FA  Accel. Intro to Programming  Miranda, Gregory Joseph  3.331  64.5  15.60  3.64  6.25  5.72  2.08   0.52   1.56
```

### Command Line Usage

```console
$ python -m asiga -h
usage: asiga [-h] [-v] [-q QUARTER] [-y YEAR] [-i INSTRUCTOR] [-s SUBJECT] [-c CODE]
```

The following command generates the grade archive of all _CSE 11_ classes (regardless of quarter and the instructor who taught the class) that occurred during the 2021 academic year:

```console
$ python -m asiga -y 21 -s CSE -c 11
  Subject  Course  Year Quarter                        Title               Instructor    GPA     A      B     C     D     F     W      P     NP
0     CSE      11    21      WI  Accel. Intro to Programming             Cao, Yingjun  3.284  37.9  22.80  4.67  1.92  2.19  6.04  14.50   6.31
1     CSE      11    21      SP  Accel. Intro to Programming  Miranda, Gregory Joseph  3.485  51.3   9.33  4.28  0.38  4.28  7.39  12.40  10.10
2     CSE      11    21      FA  Accel. Intro to Programming     Politz, Joseph Gibbs  3.484  68.4  18.20  2.61  3.39  4.43  1.56   0.78   0.52
3     CSE      11    21      FA  Accel. Intro to Programming  Miranda, Gregory Joseph  3.331  64.5  15.60  3.64  6.25  5.72  2.08   0.52   1.56
```

## Requirements

Requires **Python 3.5+**.

Dependencies:

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4)
- [html5lib](https://pypi.org/project/html5lib)
- [lxml](https://pypi.org/project/lxml)
- [pandas](https://pypi.org/project/pandas)
- [requests](https://pypi.org/project/requests)

See the project [Pipfile](https://github.com/JacobLee23/UCSD-AS-IGA/blob/master/Pipfile) for a full list of dependencies, including development dependencies.

## Installation

### Installing from PyPI

```console
$ python -m pip install ucsdasiga
```

### Installing from GitHub

First, clone the repository:

```console
$ git clone git://github.com/JacobLee23/UCSD-AS-IGA.git
```

After obtaining a copy of the source code, it can be embedded in a Python package. Or, it can be installed into `site-package`:

```console
$ cd ucsdasiga
$ python -m pip install .
```

Refer to the [Python documentation](https://docs.python.org/3/installing/index.html) for additional help installing Python modules.

***

## Notices of Non-Affiliation and Disclaimer

_This project is not endorsed by, directly affiliated with, maintained, authorized, or sponsored by the University of California, San Diego. All product and company names are the registered trademarks of their original owners. The official University of California, San Diego website can be found at https://ucsd.edu/._

_This project is not endorsed by, directly affiliated with, maintained, authorized, or sponsored by Associated Students, UC San Diego. All product and company names are the registered trademarks of their original owners. The official Associated Students, UC San Diego website can be found at https://as.ucsd.edu/._