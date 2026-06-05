# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydata/pydata-sphinx-theme/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------ | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydata\_sphinx\_theme/\_\_init\_\_.py |      142 |       17 |       58 |       12 |     84% |44, 53-\>61, 55, 61-\>65, 81-82, 88-89, 148, 163, 180, 183, 220-\>231, 222-\>231, 232-241, 291-292 |
| src/pydata\_sphinx\_theme/logo.py         |       41 |        1 |       18 |        1 |     97% |        76 |
| src/pydata\_sphinx\_theme/pygments.py     |       45 |        1 |       16 |        2 |     95% |75, 87-\>92 |
| src/pydata\_sphinx\_theme/short\_link.py  |       55 |        1 |       32 |        5 |     93% |91-\>93, 96-\>123, 99-\>123, 112, 115-\>123 |
| src/pydata\_sphinx\_theme/toctree.py      |      222 |       12 |      108 |       15 |     92% |93-96, 100-\>exit, 211-212, 346, 353, 373-\>371, 376, 378-\>412, 395-\>399, 440-\>438, 461, 472, 508, 615, 634-\>622, 641 |
| src/pydata\_sphinx\_theme/translator.py   |       42 |       20 |       14 |        2 |     46% |42-65, 72-73, 88, 93-95, 107-116 |
| src/pydata\_sphinx\_theme/utils.py        |       65 |        3 |       30 |        2 |     93% |29-32, 78-\>exit |
| **TOTAL**                                 |  **639** |   **55** |  **286** |   **39** | **89%** |           |

1 file skipped due to complete coverage.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/pydata/pydata-sphinx-theme/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/pydata/pydata-sphinx-theme/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydata/pydata-sphinx-theme/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/pydata/pydata-sphinx-theme/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fpydata%2Fpydata-sphinx-theme%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/pydata/pydata-sphinx-theme/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.