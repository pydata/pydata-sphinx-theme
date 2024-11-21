# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydata/pydata-sphinx-theme/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------ | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydata\_sphinx\_theme/\_\_init\_\_.py |      130 |       16 |       52 |       10 |     85% |44, 50->54, 70-71, 77-78, 131, 146, 163, 166, 203->214, 205->214, 215-224, 268-269 |
| src/pydata\_sphinx\_theme/logo.py         |       41 |        1 |       18 |        1 |     97% |        76 |
| src/pydata\_sphinx\_theme/pygments.py     |       45 |        1 |       16 |        2 |     95% |75, 87->92 |
| src/pydata\_sphinx\_theme/short\_link.py  |       55 |        1 |       32 |        6 |     92% |52->47, 91->93, 96->123, 99->123, 112, 115->123 |
| src/pydata\_sphinx\_theme/toctree.py      |      229 |       14 |      110 |       17 |     91% |48, 98-101, 105->exit, 141, 221-222, 349, 356, 376->374, 379, 381->415, 398->402, 443->441, 464, 475, 511, 618, 637->625, 644 |
| src/pydata\_sphinx\_theme/translator.py   |       42 |       21 |       14 |        1 |     43% |42-65, 72-73, 89-91, 103-116 |
| src/pydata\_sphinx\_theme/utils.py        |       65 |        3 |       30 |        2 |     93% |25-28, 74->exit |
|                                 **TOTAL** |  **634** |   **57** |  **282** |   **39** | **88%** |           |

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