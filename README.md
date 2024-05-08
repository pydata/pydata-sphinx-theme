# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydata/pydata-sphinx-theme/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                          |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydata\_sphinx\_theme/\_\_init\_\_.py     |      122 |       15 |       46 |        9 |     85% |31, 37->41, 57-58, 64-65, 118, 133, 150, 187->198, 189->198, 199-208, 251-252 |
| src/pydata\_sphinx\_theme/edit\_this\_page.py |       27 |        0 |       11 |        0 |    100% |           |
| src/pydata\_sphinx\_theme/logo.py             |       38 |        1 |       18 |        1 |     96% |        73 |
| src/pydata\_sphinx\_theme/pygment.py          |       45 |        1 |       18 |        2 |     95% |75, 87->92 |
| src/pydata\_sphinx\_theme/short\_link.py      |       50 |        0 |       28 |        5 |     94% |48->43, 88->90, 93->114, 96->114, 106->114 |
| src/pydata\_sphinx\_theme/toctree.py          |      211 |       12 |      114 |       15 |     92% |82-85, 89->exit, 122-123, 293, 300, 320->318, 323, 325->359, 342->346, 387->385, 408, 419, 455, 558, 577->565, 584 |
| src/pydata\_sphinx\_theme/translator.py       |       48 |       19 |       18 |        2 |     50% |36, 62-85, 107-120 |
| src/pydata\_sphinx\_theme/utils.py            |       65 |        3 |       35 |        2 |     93% |24-27, 73->exit |
|                                     **TOTAL** |  **606** |   **51** |  **288** |   **36** | **88%** |           |


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