# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydata/pydata-sphinx-theme/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------ | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydata\_sphinx\_theme/\_\_init\_\_.py |      130 |       16 |       52 |       10 |     85% |41, 47->51, 67-68, 74-75, 128, 143, 160, 163, 200->211, 202->211, 212-221, 264-265 |
| src/pydata\_sphinx\_theme/logo.py         |       41 |        1 |       18 |        1 |     97% |        74 |
| src/pydata\_sphinx\_theme/pygments.py     |       45 |        1 |       18 |        2 |     95% |75, 87->92 |
| src/pydata\_sphinx\_theme/short\_link.py  |       55 |        1 |       32 |        6 |     92% |48->43, 87->89, 92->119, 95->119, 108, 111->119 |
| src/pydata\_sphinx\_theme/toctree.py      |      229 |       14 |      122 |       17 |     91% |44, 94-97, 101->exit, 135, 215-216, 332, 339, 359->357, 362, 364->398, 381->385, 426->424, 447, 458, 494, 597, 616->604, 623 |
| src/pydata\_sphinx\_theme/translator.py   |       42 |       21 |       16 |        1 |     41% |41-67, 71-72, 94-107 |
| src/pydata\_sphinx\_theme/utils.py        |       65 |        3 |       35 |        2 |     93% |24-27, 73->exit |
|                                 **TOTAL** |  **634** |   **57** |  **304** |   **39** | **88%** |           |

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