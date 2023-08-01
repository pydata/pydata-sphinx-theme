# Expected build warnings

In our CI workflow, we use a script to check for any warnings raised by Sphinx to assert that the only warnings are _expected_ ones. The list of expected warnings can be found in :code:`tests/warning_list.txt`. To add a new entry, copy/paste the warning message (the message beginning with :code:`WARNING:`) to the bottom of the file.

For example if you get:

```console
Unexpected warning: C:\hostedtoolcache\windows\Python\3.9.13\x64\lib\site-packages\pandas\core\frame.py:docstring of pandas.core.frame.DataFrame.groupby:42: WARNING: undefined label: 'groupby.transform'
```

Add the following to the txt file:

```
WARNING: undefined label: 'groupby.transform'
```
