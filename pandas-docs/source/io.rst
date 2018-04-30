.. _io:

.. currentmodule:: pandas

.. ipython:: python
   :suppress:

   import os
   import csv
   from pandas.compat import StringIO, BytesIO
   import pandas as pd
   ExcelWriter = pd.ExcelWriter

   import numpy as np
   np.random.seed(123456)
   randn = np.random.randn
   np.set_printoptions(precision=4, suppress=True)

   import matplotlib.pyplot as plt
   plt.close('all')

   import pandas.util.testing as tm
   pd.options.display.max_rows = 15
   clipdf = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': ['p', 'q', 'r']},
                         index=['x', 'y', 'z'])

===============================
IO Tools (Text, CSV, HDF5, ...)
===============================

.. _io.read_csv_table:

CSV & Text files
----------------

The two workhorse functions for reading text files (a.k.a. flat files) are
:func:`read_csv` and :func:`read_table`. They both use the same parsing code to
intelligently convert tabular data into a ``DataFrame`` object. See the
:ref:`cookbook<cookbook.csv>` for some advanced strategies.

Parsing options
'''''''''''''''

The functions :func:`read_csv` and :func:`read_table` accept the following
common arguments:

Basic
+++++

filepath_or_buffer : various
  Either a path to a file (a :class:`python:str`, :class:`python:pathlib.Path`,
  or :class:`py:py._path.local.LocalPath`), URL (including http, ftp, and S3
  locations), or any object with a ``read()`` method (such as an open file or
  :class:`~python:io.StringIO`).
sep : str, defaults to ``','`` for :func:`read_csv`, ``\t`` for :func:`read_table`
  Delimiter to use. If sep is ``None``, the C engine cannot automatically detect
  the separator, but the Python parsing engine can, meaning the latter will be
  used and automatically detect the separator by Python's builtin sniffer tool,
  :class:`python:csv.Sniffer`. In addition, separators longer than 1 character and
  different from ``'\s+'`` will be interpreted as regular expressions and
  will also force the use of the Python parsing engine. Note that regex
  delimiters are prone to ignoring quoted data. Regex example: ``'\\r\\t'``.
delimiter : str, default ``None``
  Alternative argument name for sep.
delim_whitespace : boolean, default False
  Specifies whether or not whitespace (e.g. ``' '`` or ``'\t'``)
  will be used as the delimiter. Equivalent to setting ``sep='\s+'``.
  If this option is set to ``True``, nothing should be passed in for the
  ``delimiter`` parameter.

  .. versionadded:: 0.18.1 support for the Python parser.

Column and Index Locations and Names
++++++++++++++++++++++++++++++++++++

header : int or list of ints, default ``'infer'``
  Row number(s) to use as the column names, and the start of the
  data. Default behavior is to infer the column names: if no names are
  passed the behavior is identical to ``header=0`` and column names
  are inferred from the first line of the file, if column names are
  passed explicitly then the behavior is identical to
  ``header=None``. Explicitly pass ``header=0`` to be able to replace
  existing names.

  The header can be a list of ints that specify row locations
  for a multi-index on the columns e.g. ``[0,1,3]``. Intervening rows
  that are not specified will be skipped (e.g. 2 in this example is
  skipped). Note that this parameter ignores commented lines and empty
  lines if ``skip_blank_lines=True``, so header=0 denotes the first
  line of data rather than the first line of the file.
names : array-like, default ``None``
  List of column names to use. If file contains no header row, then you should
  explicitly pass ``header=None``. Duplicates in this list will cause
  a ``UserWarning`` to be issued.
index_col :  int or sequence or ``False``, default ``None``
  Column to use as the row labels of the ``DataFrame``. If a sequence is given, a
  MultiIndex is used. If you have a malformed file with delimiters at the end of
  each line, you might consider ``index_col=False`` to force pandas to *not* use
  the first column as the index (row names).
usecols : list-like or callable, default ``None``
  Return a subset of the columns. If list-like, all elements must either
  be positional (i.e. integer indices into the document columns) or strings
  that correspond to column names provided either by the user in `names` or
  inferred from the document header row(s). For example, a valid list-like
  `usecols` parameter would be ``[0, 1, 2]`` or ``['foo', 'bar', 'baz']``.

  Element order is ignored, so ``usecols=[0, 1]`` is the same as ``[1, 0]``. To
  instantiate a DataFrame from ``data`` with element order preserved use
  ``pd.read_csv(data, usecols=['foo', 'bar'])[['foo', 'bar']]`` for columns
  in ``['foo', 'bar']`` order or
  ``pd.read_csv(data, usecols=['foo', 'bar'])[['bar', 'foo']]`` for
  ``['bar', 'foo']`` order.

  If callable, the callable function will be evaluated against the column names,
  returning names where the callable function evaluates to True:

  .. ipython:: python

     data = 'col1,col2,col3\na,b,1\na,b,2\nc,d,3'
     pd.read_csv(StringIO(data))
     pd.read_csv(StringIO(data), usecols=lambda x: x.upper() in ['COL1', 'COL3'])

  Using this parameter results in much faster parsing time and lower memory usage.
squeeze : boolean, default ``False``
  If the parsed data only contains one column then return a ``Series``.
prefix : str, default ``None``
  Prefix to add to column numbers when no header, e.g. 'X' for X0, X1, ...
mangle_dupe_cols : boolean, default ``True``
  Duplicate columns will be specified as 'X', 'X.1'...'X.N', rather than 'X'...'X'.
  Passing in ``False`` will cause data to be overwritten if there are duplicate
  names in the columns.

General Parsing Configuration
+++++++++++++++++++++++++++++

dtype : Type name or dict of column -> type, default ``None``
  Data type for data or columns. E.g. ``{'a': np.float64, 'b': np.int32}``
  (unsupported with ``engine='python'``). Use `str` or `object` to preserve and
  not interpret dtype.

  .. versionadded:: 0.20.0 support for the Python parser.

engine : {``'c'``, ``'python'``}
  Parser engine to use. The C engine is faster while the Python engine is
  currently more feature-complete.
converters : dict, default ``None``
  Dict of functions for converting values in certain columns. Keys can either be
  integers or column labels.
true_values : list, default ``None``
  Values to consider as ``True``.
false_values : list, default ``None``
  Values to consider as ``False``.
skipinitialspace : boolean, default ``False``
  Skip spaces after delimiter.
skiprows : list-like or integer, default ``None``
  Line numbers to skip (0-indexed) or number of lines to skip (int) at the start
  of the file.

  If callable, the callable function will be evaluated against the row
  indices, returning True if the row should be skipped and False otherwise:

  .. ipython:: python

     data = 'col1,col2,col3\na,b,1\na,b,2\nc,d,3'
     pd.read_csv(StringIO(data))
     pd.read_csv(StringIO(data), skiprows=lambda x: x % 2 != 0)

skipfooter : int, default ``0``
  Number of lines at bottom of file to skip (unsupported with engine='c').

nrows : int, default ``None``
  Number of rows of file to read. Useful for reading pieces of large files.
low_memory : boolean, default ``True``
  Internally process the file in chunks, resulting in lower memory use
  while parsing, but possibly mixed type inference.  To ensure no mixed
  types either set ``False``, or specify the type with the ``dtype`` parameter.
  Note that the entire file is read into a single ``DataFrame`` regardless,
  use the ``chunksize`` or ``iterator`` parameter to return the data in chunks.
  (Only valid with C parser)
memory_map : boolean, default False
  If a filepath is provided for ``filepath_or_buffer``, map the file object
  directly onto memory and access the data directly from there. Using this
  option can improve performance because there is no longer any I/O overhead.

NA and Missing Data Handling
++++++++++++++++++++++++++++

na_values : scalar, str, list-like, or dict, default ``None``
  Additional strings to recognize as NA/NaN. If dict passed, specific per-column
  NA values. See :ref:`na values const <io.navaluesconst>` below
  for a list of the values interpreted as NaN by default.

keep_default_na : boolean, default ``True``
  Whether or not to include the default NaN values when parsing the data.
  Depending on whether `na_values` is passed in, the behavior is as follows:

  * If `keep_default_na` is ``True``, and `na_values` are specified, `na_values`
    is appended to the default NaN values used for parsing.
  * If `keep_default_na` is ``True``, and `na_values` are not specified, only
    the default NaN values are used for parsing.
  * If `keep_default_na` is ``False``, and `na_values` are specified, only
    the NaN values specified `na_values` are used for parsing.
  * If `keep_default_na` is ``False``, and `na_values` are not specified, no
    strings will be parsed as NaN.

  Note that if `na_filter` is passed in as ``False``, the `keep_default_na` and
  `na_values` parameters will be ignored.
na_filter : boolean, default ``True``
  Detect missing value markers (empty strings and the value of na_values). In
  data without any NAs, passing ``na_filter=False`` can improve the performance
  of reading a large file.
verbose : boolean, default ``False``
  Indicate number of NA values placed in non-numeric columns.
skip_blank_lines : boolean, default ``True``
  If ``True``, skip over blank lines rather than interpreting as NaN values.

Datetime Handling
+++++++++++++++++

parse_dates : boolean or list of ints or names or list of lists or dict, default ``False``.
  - If ``True`` -> try parsing the index.
  - If ``[1, 2, 3]`` ->  try parsing columns 1, 2, 3 each as a separate date
    column.
  - If ``[[1, 3]]`` -> combine columns 1 and 3 and parse as a single date
    column.
  - If ``{'foo': [1, 3]}`` -> parse columns 1, 3 as date and call result 'foo'.
    A fast-path exists for iso8601-formatted dates.
infer_datetime_format : boolean, default ``False``
  If ``True`` and parse_dates is enabled for a column, attempt to infer the
  datetime format to speed up the processing.
keep_date_col : boolean, default ``False``
  If ``True`` and parse_dates specifies combining multiple columns then keep the
  original columns.
date_parser : function, default ``None``
  Function to use for converting a sequence of string columns to an array of
  datetime instances. The default uses ``dateutil.parser.parser`` to do the
  conversion. Pandas will try to call date_parser in three different ways,
  advancing to the next if an exception occurs: 1) Pass one or more arrays (as
  defined by parse_dates) as arguments; 2) concatenate (row-wise) the string
  values from the columns defined by parse_dates into a single array and pass
  that; and 3) call date_parser once for each row using one or more strings
  (corresponding to the columns defined by parse_dates) as arguments.
dayfirst : boolean, default ``False``
  DD/MM format dates, international and European format.

Iteration
+++++++++

iterator : boolean, default ``False``
  Return `TextFileReader` object for iteration or getting chunks with
  ``get_chunk()``.
chunksize : int, default ``None``
  Return `TextFileReader` object for iteration. See :ref:`iterating and chunking
  <io.chunking>` below.

Quoting, Compression, and File Format
+++++++++++++++++++++++++++++++++++++

compression : {``'infer'``, ``'gzip'``, ``'bz2'``, ``'zip'``, ``'xz'``, ``None``}, default ``'infer'``
  For on-the-fly decompression of on-disk data. If 'infer', then use gzip,
  bz2, zip, or xz if filepath_or_buffer is a string ending in '.gz', '.bz2',
  '.zip', or '.xz', respectively, and no decompression otherwise. If using 'zip',
  the ZIP file must contain only one data file to be read in.
  Set to ``None`` for no decompression.

  .. versionadded:: 0.18.1 support for 'zip' and 'xz' compression.

thousands : str, default ``None``
  Thousands separator.
decimal : str, default ``'.'``
  Character to recognize as decimal point. E.g. use ``','`` for European data.
float_precision : string, default None
  Specifies which converter the C engine should use for floating-point values.
  The options are ``None`` for the ordinary converter, ``high`` for the
  high-precision converter, and ``round_trip`` for the round-trip converter.
lineterminator : str (length 1), default ``None``
  Character to break file into lines. Only valid with C parser.
quotechar : str (length 1)
  The character used to denote the start and end of a quoted item. Quoted items
  can include the delimiter and it will be ignored.
quoting : int or ``csv.QUOTE_*`` instance, default ``0``
  Control field quoting behavior per ``csv.QUOTE_*`` constants. Use one of
  ``QUOTE_MINIMAL`` (0), ``QUOTE_ALL`` (1), ``QUOTE_NONNUMERIC`` (2) or
  ``QUOTE_NONE`` (3).
doublequote : boolean, default ``True``
   When ``quotechar`` is specified and ``quoting`` is not ``QUOTE_NONE``,
   indicate whether or not to interpret two consecutive ``quotechar`` elements
   **inside** a field as a single ``quotechar`` element.
escapechar : str (length 1), default ``None``
  One-character string used to escape delimiter when quoting is ``QUOTE_NONE``.
comment : str, default ``None``
  Indicates remainder of line should not be parsed. If found at the beginning of
  a line, the line will be ignored altogether. This parameter must be a single
  character. Like empty lines (as long as ``skip_blank_lines=True``), fully
  commented lines are ignored by the parameter `header` but not by `skiprows`.
  For example, if ``comment='#'``, parsing '#empty\\na,b,c\\n1,2,3' with
  `header=0` will result in 'a,b,c' being treated as the header.
encoding : str, default ``None``
  Encoding to use for UTF when reading/writing (e.g. ``'utf-8'``). `List of
  Python standard encodings
  <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.
dialect : str or :class:`python:csv.Dialect` instance, default ``None``
  If provided, this parameter will override values (default or not) for the
  following parameters: `delimiter`, `doublequote`, `escapechar`,
  `skipinitialspace`, `quotechar`, and `quoting`. If it is necessary to
  override values, a ParserWarning will be issued. See :class:`python:csv.Dialect`
  documentation for more details.
tupleize_cols : boolean, default ``False``
    .. deprecated:: 0.21.0

    This argument will be removed and will always convert to MultiIndex

  Leave a list of tuples on columns as is (default is to convert to a MultiIndex
  on the columns).

Error Handling
++++++++++++++

error_bad_lines : boolean, default ``True``
  Lines with too many fields (e.g. a csv line with too many commas) will by
  default cause an exception to be raised, and no ``DataFrame`` will be
  returned. If ``False``, then these "bad lines" will dropped from the
  ``DataFrame`` that is returned. See :ref:`bad lines <io.bad_lines>`
  below.
warn_bad_lines : boolean, default ``True``
  If error_bad_lines is ``False``, and warn_bad_lines is ``True``, a warning for
  each "bad line" will be output.

.. _io.dtypes:

Specifying column data types
''''''''''''''''''''''''''''

You can indicate the data type for the whole ``DataFrame`` or individual
columns:

.. ipython:: python

    data = 'a,b,c\n1,2,3\n4,5,6\n7,8,9'
    print(data)

    df = pd.read_csv(StringIO(data), dtype=object)
    df
    df['a'][0]
    df = pd.read_csv(StringIO(data), dtype={'b': object, 'c': np.float64})
    df.dtypes

Fortunately, pandas offers more than one way to ensure that your column(s)
contain only one ``dtype``. If you're unfamiliar with these concepts, you can
see :ref:`here<basics.dtypes>` to learn more about dtypes, and
:ref:`here<basics.object_conversion>` to learn more about ``object`` conversion in
pandas.


For instance, you can use the ``converters`` argument
of :func:`~pandas.read_csv`:

.. ipython:: python

    data = "col_1\n1\n2\n'A'\n4.22"
    df = pd.read_csv(StringIO(data), converters={'col_1': str})
    df
    df['col_1'].apply(type).value_counts()

Or you can use the :func:`~pandas.to_numeric` function to coerce the
dtypes after reading in the data,

.. ipython:: python

    df2 = pd.read_csv(StringIO(data))
    df2['col_1'] = pd.to_numeric(df2['col_1'], errors='coerce')
    df2
    df2['col_1'].apply(type).value_counts()

which will convert all valid parsing to floats, leaving the invalid parsing
as ``NaN``.

Ultimately, how you deal with reading in columns containing mixed dtypes
depends on your specific needs. In the case above, if you wanted to ``NaN`` out
the data anomalies, then :func:`~pandas.to_numeric` is probably your best option.
However, if you wanted for all the data to be coerced, no matter the type, then
using the ``converters`` argument of :func:`~pandas.read_csv` would certainly be
worth trying.

  .. versionadded:: 0.20.0 support for the Python parser.

     The ``dtype`` option is supported by the 'python' engine.

.. note::
   In some cases, reading in abnormal data with columns containing mixed dtypes
   will result in an inconsistent dataset. If you rely on pandas to infer the
   dtypes of your columns, the parsing engine will go and infer the dtypes for
   different chunks of the data, rather than the whole dataset at once. Consequently,
   you can end up with column(s) with mixed dtypes. For example,

   .. ipython:: python
        :okwarning:

        df = pd.DataFrame({'col_1': list(range(500000)) + ['a', 'b'] + list(range(500000))})
        df.to_csv('foo.csv')
        mixed_df = pd.read_csv('foo.csv')
        mixed_df['col_1'].apply(type).value_counts()
        mixed_df['col_1'].dtype

   will result with `mixed_df` containing an ``int`` dtype for certain chunks
   of the column, and ``str`` for others due to the mixed dtypes from the
   data that was read in. It is important to note that the overall column will be
   marked with a ``dtype`` of ``object``, which is used for columns with mixed dtypes.

.. ipython:: python
   :suppress:

   os.remove('foo.csv')

.. _io.categorical:

Specifying Categorical dtype
''''''''''''''''''''''''''''

.. versionadded:: 0.19.0

``Categorical`` columns can be parsed directly by specifying ``dtype='category'`` or
``dtype=CategoricalDtype(categories, ordered)``.

.. ipython:: python

   data = 'col1,col2,col3\na,b,1\na,b,2\nc,d,3'

   pd.read_csv(StringIO(data))
   pd.read_csv(StringIO(data)).dtypes
   pd.read_csv(StringIO(data), dtype='category').dtypes

Individual columns can be parsed as a ``Categorical`` using a dict
specification:

.. ipython:: python

   pd.read_csv(StringIO(data), dtype={'col1': 'category'}).dtypes

.. versionadded:: 0.21.0

Specifying ``dtype='cateogry'`` will result in an unordered ``Categorical``
whose ``categories`` are the unique values observed in the data. For more
control on the categories and order, create a
:class:`~pandas.api.types.CategoricalDtype` ahead of time, and pass that for
that column's ``dtype``.

.. ipython:: python

   from pandas.api.types import CategoricalDtype

   dtype = CategoricalDtype(['d', 'c', 'b', 'a'], ordered=True)
   pd.read_csv(StringIO(data), dtype={'col1': dtype}).dtypes

When using ``dtype=CategoricalDtype``, "unexpected" values outside of
``dtype.categories`` are treated as missing values.

.. ipython:: python

   dtype = CategoricalDtype(['a', 'b', 'd'])  # No 'c'
   pd.read_csv(StringIO(data), dtype={'col1': dtype}).col1

This matches the behavior of :meth:`Categorical.set_categories`.

.. note::

   With ``dtype='category'``, the resulting categories will always be parsed
   as strings (object dtype). If the categories are numeric they can be
   converted using the :func:`to_numeric` function, or as appropriate, another
   converter such as :func:`to_datetime`.

   When ``dtype`` is a ``CategoricalDtype`` with homogenous ``categories`` (
   all numeric, all datetimes, etc.), the conversion is done automatically.

   .. ipython:: python

      df = pd.read_csv(StringIO(data), dtype='category')
      df.dtypes
      df['col3']
      df['col3'].cat.categories = pd.to_numeric(df['col3'].cat.categories)
      df['col3']

