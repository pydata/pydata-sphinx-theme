.. _indexing:


********************************************
Pandas example - Indexing and selecting data
********************************************

.. note::

    This is an example page with excerpts from the pandas docs, for some "real world" content.
    But including it here apart from the rest of the pandas docs will mean that some of the links won't work, and not all code
    examples are shown with their complete outputs.


The axis labeling information in pandas objects serves many purposes:

* Identifies data (i.e. provides *metadata*) using known indicators,
  important for analysis, visualization, and interactive console display.
* Enables automatic and explicit data alignment.
* Allows intuitive getting and setting of subsets of the data set.

In this section, we will focus on the final point: namely, how to slice, dice,
and generally get and set subsets of pandas objects. The primary focus will be
on Series and DataFrame as they have received more development attention in
this area.

.. note::

   The Python and NumPy indexing operators ``[]`` and attribute operator ``.``
   provide quick and easy access to pandas data structures across a wide range
   of use cases. This makes interactive work intuitive, as there's little new
   to learn if you already know how to deal with Python dictionaries and NumPy
   arrays. However, since the type of the data to be accessed isn't known in
   advance, directly using standard operators has some optimization limits. For
   production code, we recommended that you take advantage of the optimized
   pandas data access methods exposed in this chapter.

.. warning::

   Whether a copy or a reference is returned for a setting operation, may
   depend on the context. This is sometimes called ``chained assignment`` and
   should be avoided. See :ref:`Returning a View versus Copy
   <indexing.view_versus_copy>`.

.. _indexing.choice:

Different choices for indexing
------------------------------

Object selection has had a number of user-requested additions in order to
support more explicit location based indexing. Pandas now supports three types
of multi-axis indexing.

* ``.loc`` is primarily label based, but may also be used with a boolean array. ``.loc`` will raise ``KeyError`` when the items are not found. Allowed inputs are:

    * A single label, e.g. ``5`` or ``'a'`` (Note that ``5`` is interpreted as a
      *label* of the index. This use is **not** an integer position along the
      index.).
    * A list or array of labels ``['a', 'b', 'c']``.
    * A slice object with labels ``'a':'f'`` (Note that contrary to usual python
      slices, **both** the start and the stop are included, when present in the
      index!)
    * A boolean array
    * A ``callable`` function with one argument (the calling Series or DataFrame) and
      that returns valid output for indexing (one of the above).

  See more at :ref:`Selection by Label <indexing.label>`.

* ``.iloc`` is primarily integer position based (from ``0`` to
  ``length-1`` of the axis), but may also be used with a boolean
  array.  ``.iloc`` will raise ``IndexError`` if a requested
  indexer is out-of-bounds, except *slice* indexers which allow
  out-of-bounds indexing.  (this conforms with Python/NumPy *slice*
  semantics).  Allowed inputs are:

    * An integer e.g. ``5``.
    * A list or array of integers ``[4, 3, 0]``.
    * A slice object with ints ``1:7``.
    * A boolean array.
    * A ``callable`` function with one argument (the calling Series or DataFrame) and
      that returns valid output for indexing (one of the above).

* ``.loc``, ``.iloc``, and also ``[]`` indexing can accept a ``callable`` as indexer. See more at :ref:`Selection By Callable <indexing.callable>`.

Getting values from an object with multi-axes selection uses the following
notation (using ``.loc`` as an example, but the following applies to ``.iloc`` as
well). Any of the axes accessors may be the null slice ``:``. Axes left out of
the specification are assumed to be ``:``, e.g. ``p.loc['a']`` is equivalent to
``p.loc['a', :, :]``.

.. csv-table::
    :header: "Object Type", "Indexers"
    :widths: 30, 50
    :delim: ;

    Series; ``s.loc[indexer]``
    DataFrame; ``df.loc[row_indexer,column_indexer]``

.. _indexing.basics:

Basics
------

As mentioned when introducing the data structures in the last section,
the primary function of indexing with ``[]`` (a.k.a. ``__getitem__``
for those familiar with implementing class behavior in Python) is selecting out
lower-dimensional slices. The following table shows return type values when
indexing pandas objects with ``[]``:

.. csv-table::
    :header: "Object Type", "Selection", "Return Value Type"
    :widths: 30, 30, 60
    :delim: ;

    Series; ``series[label]``; scalar value
    DataFrame; ``frame[colname]``; ``Series`` corresponding to colname

Here we construct a simple time series data set to use for illustrating the
indexing functionality:

.. code-block:: python

    >>> dates = pd.date_range('1/1/2000', periods=8)

    >>> df = pd.DataFrame(np.random.randn(8, 4),
    ...                   index=dates, columns=['A', 'B', 'C', 'D'])
    ...

    >>> df
                    A         B         C         D
    2000-01-01  0.469112 -0.282863 -1.509059 -1.135632
    2000-01-02  1.212112 -0.173215  0.119209 -1.044236
    2000-01-03 -0.861849 -2.104569 -0.494929  1.071804
    2000-01-04  0.721555 -0.706771 -1.039575  0.271860
    2000-01-05 -0.424972  0.567020  0.276232 -1.087401
    2000-01-06 -0.673690  0.113648 -1.478427  0.524988
    2000-01-07  0.404705  0.577046 -1.715002 -1.039268
    2000-01-08 -0.370647 -1.157892 -1.344312  0.844885

.. note::

   None of the indexing functionality is time series specific unless
   specifically stated.

Thus, as per above, we have the most basic indexing using ``[]``:

.. code-block:: python

    >>> s = df['A']

    >>> s[dates[5]]
    -0.6736897080883706


You can pass a list of columns to ``[]`` to select columns in that order.
If a column is not contained in the DataFrame, an exception will be
raised. Multiple columns can also be set in this manner:

.. code-block:: python

    >>> df
                    A         B         C         D
    2000-01-01  0.469112 -0.282863 -1.509059 -1.135632
    2000-01-02  1.212112 -0.173215  0.119209 -1.044236
    2000-01-03 -0.861849 -2.104569 -0.494929  1.071804
    2000-01-04  0.721555 -0.706771 -1.039575  0.271860
    2000-01-05 -0.424972  0.567020  0.276232 -1.087401
    2000-01-06 -0.673690  0.113648 -1.478427  0.524988
    2000-01-07  0.404705  0.577046 -1.715002 -1.039268
    2000-01-08 -0.370647 -1.157892 -1.344312  0.844885

    >>> df[['B', 'A']] = df[['A', 'B']]

    >>> df
                    A         B         C         D
    2000-01-01 -0.282863  0.469112 -1.509059 -1.135632
    2000-01-02 -0.173215  1.212112  0.119209 -1.044236
    2000-01-03 -2.104569 -0.861849 -0.494929  1.071804
    2000-01-04 -0.706771  0.721555 -1.039575  0.271860
    2000-01-05  0.567020 -0.424972  0.276232 -1.087401
    2000-01-06  0.113648 -0.673690 -1.478427  0.524988
    2000-01-07  0.577046  0.404705 -1.715002 -1.039268
    2000-01-08 -1.157892 -0.370647 -1.344312  0.844885

You may find this useful for applying a transform (in-place) to a subset of the
columns.

.. warning::

   pandas aligns all AXES when setting ``Series`` and ``DataFrame`` from ``.loc``, and ``.iloc``.

   This will **not** modify ``df`` because the column alignment is before value assignment.

   .. code-block:: python

        >>> df[['A', 'B']]
                        A         B
        2000-01-01 -0.282863  0.469112
        2000-01-02 -0.173215  1.212112
        2000-01-03 -2.104569 -0.861849
        2000-01-04 -0.706771  0.721555
        2000-01-05  0.567020 -0.424972
        2000-01-06  0.113648 -0.673690
        2000-01-07  0.577046  0.404705
        2000-01-08 -1.157892 -0.370647

        >>> df.loc[:, ['B', 'A']] = df[['A', 'B']]

        >>> df[['A', 'B']]
                        A         B
        2000-01-01 -0.282863  0.469112
        2000-01-02 -0.173215  1.212112
        2000-01-03 -2.104569 -0.861849
        2000-01-04 -0.706771  0.721555
        2000-01-05  0.567020 -0.424972
        2000-01-06  0.113648 -0.673690
        2000-01-07  0.577046  0.404705
        2000-01-08 -1.157892 -0.370647

   The correct way to swap column values is by using raw values:

   .. code-block:: python

        >>> df.loc[:, ['B', 'A']] = df[['A', 'B']].to_numpy()

        >>> df[['A', 'B']]
                        A         B
        2000-01-01  0.469112 -0.282863
        2000-01-02  1.212112 -0.173215
        2000-01-03 -0.861849 -2.104569
        2000-01-04  0.721555 -0.706771
        2000-01-05 -0.424972  0.567020
        2000-01-06 -0.673690  0.113648
        2000-01-07  0.404705  0.577046
        2000-01-08 -0.370647 -1.157892


Attribute access
----------------

.. _indexing.columns.multiple:

.. _indexing.df_cols:

.. _indexing.attribute_access:

You may access an index on a ``Series`` or  column on a ``DataFrame`` directly
as an attribute:

.. code-block:: python

   sa = pd.Series([1, 2, 3], index=list('abc'))
   dfa = df.copy()

.. code-block:: python

   sa.b
   dfa.A

.. code-block:: python

    >>> sa.a = 5

    >>> sa
    a    5
    b    2
    c    3
    dtype: int64

    >>> dfa.A = list(range(len(dfa.index)))  # ok if A already exists

    >>> dfa
                A         B         C         D
    2000-01-01  0 -0.282863 -1.509059 -1.135632
    2000-01-02  1 -0.173215  0.119209 -1.044236
    2000-01-03  2 -2.104569 -0.494929  1.071804
    2000-01-04  3 -0.706771 -1.039575  0.271860
    2000-01-05  4  0.567020  0.276232 -1.087401
    2000-01-06  5  0.113648 -1.478427  0.524988
    2000-01-07  6  0.577046 -1.715002 -1.039268
    2000-01-08  7 -1.157892 -1.344312  0.844885

    >>> dfa['A'] = list(range(len(dfa.index)))  # use this form to create a new column

    >>> dfa
                A         B         C         D
    2000-01-01  0 -0.282863 -1.509059 -1.135632
    2000-01-02  1 -0.173215  0.119209 -1.044236
    2000-01-03  2 -2.104569 -0.494929  1.071804
    2000-01-04  3 -0.706771 -1.039575  0.271860
    2000-01-05  4  0.567020  0.276232 -1.087401
    2000-01-06  5  0.113648 -1.478427  0.524988
    2000-01-07  6  0.577046 -1.715002 -1.039268
    2000-01-08  7 -1.157892 -1.344312  0.844885

.. warning::

   - You can use this access only if the index element is a valid Python identifier, e.g. ``s.1`` is not allowed.
     See `here for an explanation of valid identifiers
     <https://docs.python.org/3/reference/lexical_analysis.html#identifiers>`__.

   - The attribute will not be available if it conflicts with an existing method name, e.g. ``s.min`` is not allowed, but ``s['min']`` is possible.

   - Similarly, the attribute will not be available if it conflicts with any of the following list: ``index``,
     ``major_axis``, ``minor_axis``, ``items``.

   - In any of these cases, standard indexing will still work, e.g. ``s['1']``, ``s['min']``, and ``s['index']`` will
     access the corresponding element or column.

If you are using the IPython environment, you may also use tab-completion to
see these accessible attributes.

You can also assign a ``dict`` to a row of a ``DataFrame``:

.. code-block:: python

    >>> x = pd.DataFrame({'x': [1, 2, 3], 'y': [3, 4, 5]})

    >>> x.iloc[1] = {'x': 9, 'y': 99}

    >>> x
    x   y
    0  1   3
    1  9  99
    2  3   5


You can use attribute access to modify an existing element of a Series or column of a DataFrame, but be careful;
if you try to use attribute access to create a new column, it creates a new attribute rather than a
new column. In 0.21.0 and later, this will raise a ``UserWarning``:

.. code-block:: python

    >>> df = pd.DataFrame({'one': [1., 2., 3.]})
    >>> df.two = [4, 5, 6]
    UserWarning: Pandas doesn't allow Series to be assigned into nonexistent columns - see https://pandas.pydata.org/pandas-docs/stable/indexing.html#attribute_access
    >>> df
       one
    0  1.0
    1  2.0
    2  3.0

.. _indexing.label:

Selection by label
------------------

.. warning::

   Whether a copy or a reference is returned for a setting operation, may depend on the context.
   This is sometimes called ``chained assignment`` and should be avoided.
   See :ref:`Returning a View versus Copy <indexing.view_versus_copy>`.

.. warning::

   ``.loc`` is strict when you present slicers that are not compatible (or convertible) with the index type. For example
   using integers in a ``DatetimeIndex``. These will raise a ``TypeError``.

  .. code-block:: python

     dfl = pd.DataFrame(np.random.randn(5, 4),
                        columns=list('ABCD'),
                        index=pd.date_range('20130101', periods=5))
     dfl

  .. code-block:: python

     >>> dfl.loc[2:3]
     TypeError: cannot do slice indexing on <class 'pandas.tseries.index.DatetimeIndex'> with these indexers [2] of <type 'int'>

  String likes in slicing *can* be convertible to the type of the index and lead to natural slicing.

  .. code-block:: python

     dfl.loc['20130102':'20130104']

pandas provides a suite of methods in order to have **purely label based indexing**. This is a strict inclusion based protocol.
Every label asked for must be in the index, or a ``KeyError`` will be raised.
When slicing, both the start bound **AND** the stop bound are *included*, if present in the index.
Integers are valid labels, but they refer to the label **and not the position**.

The ``.loc`` attribute is the primary access method. The following are valid inputs:

* A single label, e.g. ``5`` or ``'a'`` (Note that ``5`` is interpreted as a *label* of the index. This use is **not** an integer position along the index.).
* A list or array of labels ``['a', 'b', 'c']``.
* A slice object with labels ``'a':'f'`` (Note that contrary to usual python
  slices, **both** the start and the stop are included, when present in the
  index! See :ref:`Slicing with labels <indexing.slicing_with_labels>`.
* A boolean array.
* A ``callable``, see :ref:`Selection By Callable <indexing.callable>`.

.. code-block:: python

    >>> s1 = pd.Series(np.random.randn(6), index=list('abcdef'))

    >>> s1
    a    1.431256
    b    1.340309
    c   -1.170299
    d   -0.226169
    e    0.410835
    f    0.813850
    dtype: float64

    >>> s1.loc['c':]
    c   -1.170299
    d   -0.226169
    e    0.410835
    f    0.813850
    dtype: float64

    >>> s1.loc['b']
    1.3403088497993827

Note that setting works as well:

.. code-block:: python

    >>> s1.loc['c':] = 0

    >>> s1
    a    1.431256
    b    1.340309
    c    0.000000
    d    0.000000
    e    0.000000
    f    0.000000
    dtype: float64

With a DataFrame:

.. code-block:: python

    >>> df1 = pd.DataFrame(np.random.randn(6, 4),
    ....                    index=list('abcdef'),
    ....                    columns=list('ABCD'))
    ....

    >>> df1
            A         B         C         D
    a  0.132003 -0.827317 -0.076467 -1.187678
    b  1.130127 -1.436737 -1.413681  1.607920
    c  1.024180  0.569605  0.875906 -2.211372
    d  0.974466 -2.006747 -0.410001 -0.078638
    e  0.545952 -1.219217 -1.226825  0.769804
    f -1.281247 -0.727707 -0.121306 -0.097883

    >>> df1.loc[['a', 'b', 'd'], :]
            A         B         C         D
    a  0.132003 -0.827317 -0.076467 -1.187678
    b  1.130127 -1.436737 -1.413681  1.607920


.. _indexing.slicing_with_labels:

Slicing with labels
~~~~~~~~~~~~~~~~~~~

When using ``.loc`` with slices, if both the start and the stop labels are
present in the index, then elements *located* between the two (including them)
are returned:

.. code-block:: python

    >>> s = pd.Series(list('abcde'), index=[0, 3, 2, 5, 4])

    >>> s.loc[3:5]
    3    b
    2    c
    5    d
    dtype: object

If at least one of the two is absent, but the index is sorted, and can be
compared against start and stop labels, then slicing will still work as
expected, by selecting labels which *rank* between the two:

.. code-block:: python

    >>> s.sort_index()
    0    a
    2    c
    3    b
    4    e
    5    d
    dtype: object

    >>> s.sort_index().loc[1:6]
    2    c
    3    b
    4    e
    5    d
    dtype: object

However, if at least one of the two is absent *and* the index is not sorted, an
error will be raised (since doing otherwise would be computationally expensive,
as well as potentially ambiguous for mixed type indexes). For instance, in the
above example, ``s.loc[1:6]`` would raise ``KeyError``.

.. _indexing.integer:

Selection by position
---------------------

.. warning::

   Whether a copy or a reference is returned for a setting operation, may depend on the context.
   This is sometimes called ``chained assignment`` and should be avoided.
   See :ref:`Returning a View versus Copy <indexing.view_versus_copy>`.

Pandas provides a suite of methods in order to get **purely integer based indexing**. The semantics follow closely Python and NumPy slicing. These are ``0-based`` indexing. When slicing, the start bound is *included*, while the upper bound is *excluded*. Trying to use a non-integer, even a **valid** label will raise an ``IndexError``.

The ``.iloc`` attribute is the primary access method. The following are valid inputs:

* An integer e.g. ``5``.
* A list or array of integers ``[4, 3, 0]``.
* A slice object with ints ``1:7``.
* A boolean array.
* A ``callable``, see :ref:`Selection By Callable <indexing.callable>`.

.. code-block:: python

    >>> s1 = pd.Series(np.random.randn(5), index=list(range(0, 10, 2)))

    >>> s1
    0    0.695775
    2    0.341734
    4    0.959726
    6   -1.110336
    8   -0.619976
    dtype: float64

    >>> s1.iloc[:3]
    0    0.695775
    2    0.341734
    4    0.959726
    dtype: float64

    >>> s1.iloc[3]
    -1.110336102891167

Note that setting works as well:

.. code-block:: python

   s1.iloc[:3] = 0
   s1

With a DataFrame:

.. code-block:: python

   df1 = pd.DataFrame(np.random.randn(6, 4),
                      index=list(range(0, 12, 2)),
                      columns=list(range(0, 8, 2)))
   df1

Select via integer slicing:

.. code-block:: python

   df1.iloc[:3]
   df1.iloc[1:5, 2:4]

Select via integer list:

.. code-block:: python

   df1.iloc[[1, 3, 5], [1, 3]]

.. code-block:: python

   df1.iloc[1:3, :]

.. code-block:: python

   df1.iloc[:, 1:3]

.. code-block:: python

   # this is also equivalent to ``df1.iat[1,1]``
   df1.iloc[1, 1]

For getting a cross section using an integer position (equiv to ``df.xs(1)``):

.. code-block:: python

   df1.iloc[1]

Out of range slice indexes are handled gracefully just as in Python/Numpy.

.. code-block:: python

    # these are allowed in python/numpy.
    x = list('abcdef')
    x
    x[4:10]
    x[8:10]
    s = pd.Series(x)
    s
    s.iloc[4:10]
    s.iloc[8:10]

Note that using slices that go out of bounds can result in
an empty axis (e.g. an empty DataFrame being returned).

.. code-block:: python

   dfl = pd.DataFrame(np.random.randn(5, 2), columns=list('AB'))
   dfl
   dfl.iloc[:, 2:3]
   dfl.iloc[:, 1:3]
   dfl.iloc[4:6]

A single indexer that is out of bounds will raise an ``IndexError``.
A list of indexers where any element is out of bounds will raise an
``IndexError``.

.. code-block:: python

   >>> dfl.iloc[[4, 5, 6]]
   IndexError: positional indexers are out-of-bounds

   >>> dfl.iloc[:, 4]
   IndexError: single positional indexer is out-of-bounds

.. _indexing.callable:

Selection by callable
---------------------

``.loc``, ``.iloc``, and also ``[]`` indexing can accept a ``callable`` as indexer.
The ``callable`` must be a function with one argument (the calling Series or DataFrame) that returns valid output for indexing.

.. code-block:: python

    >>> df1 = pd.DataFrame(np.random.randn(6, 4),
    ....                    index=list('abcdef'),
    ....                    columns=list('ABCD'))
    ....

    >>> df1
            A         B         C         D
    a -0.023688  2.410179  1.450520  0.206053
    b -0.251905 -2.213588  1.063327  1.266143
    c  0.299368 -0.863838  0.408204 -1.048089
    d -0.025747 -0.988387  0.094055  1.262731
    e  1.289997  0.082423 -0.055758  0.536580
    f -0.489682  0.369374 -0.034571 -2.484478

    >>> df1.loc[lambda df: df['A'] > 0, :]
            A         B         C         D
    c  0.299368 -0.863838  0.408204 -1.048089
    e  1.289997  0.082423 -0.055758  0.536580

    >>> df1.loc[:, lambda df: ['A', 'B']]
            A         B
    a -0.023688  2.410179
    b -0.251905 -2.213588
    c  0.299368 -0.863838
    d -0.025747 -0.988387
    e  1.289997  0.082423
    f -0.489682  0.369374

    >>> df1.iloc[:, lambda df: [0, 1]]
            A         B
    a -0.023688  2.410179
    b -0.251905 -2.213588
    c  0.299368 -0.863838
    d -0.025747 -0.988387
    e  1.289997  0.082423
    f -0.489682  0.369374

    >>> df1[lambda df: df.columns[0]]
    a   -0.023688
    b   -0.251905
    c    0.299368
    d   -0.025747
    e    1.289997
    f   -0.489682
    Name: A, dtype: float64



You can use callable indexing in ``Series``.

.. code-block:: python

   df1['A'].loc[lambda s: s > 0]

Using these methods / indexers, you can chain data selection operations
without using a temporary variable.

.. code-block:: python

   bb = pd.read_csv('data/baseball.csv', index_col='id')
   (bb.groupby(['year', 'team']).sum()
      .loc[lambda df: df['r'] > 100])


Boolean indexing
----------------

.. _indexing.boolean:

Another common operation is the use of boolean vectors to filter the data.
The operators are: ``|`` for ``or``, ``&`` for ``and``, and ``~`` for ``not``.
These **must** be grouped by using parentheses, since by default Python will
evaluate an expression such as ``df['A'] > 2 & df['B'] < 3`` as
``df['A'] > (2 & df['B']) < 3``, while the desired evaluation order is
``(df['A > 2) & (df['B'] < 3)``.

Using a boolean vector to index a Series works exactly as in a NumPy ndarray:

.. code-block:: python

    >>> s = pd.Series(range(-3, 4))

    >>> s
    0   -3
    1   -2
    2   -1
    3    0
    4    1
    5    2
    6    3
    dtype: int64

    >>> s[s > 0]
    4    1
    5    2
    6    3
    dtype: int64

    >>> s[(s < -1) | (s > 0.5)]
    0   -3
    1   -2
    4    1
    5    2
    6    3
    dtype: int64

    >>> s[~(s < 0)]
    3    0
    4    1
    5    2
    6    3
    dtype: int64

You may select rows from a DataFrame using a boolean vector the same length as
the DataFrame's index (for example, something derived from one of the columns
of the DataFrame):

.. code-block:: python

   df[df['A'] > 0]

List comprehensions and the ``map`` method of Series can also be used to produce
more complex criteria:

.. code-block:: python

   df2 = pd.DataFrame({'a': ['one', 'one', 'two', 'three', 'two', 'one', 'six'],
                       'b': ['x', 'y', 'y', 'x', 'y', 'x', 'x'],
                       'c': np.random.randn(7)})

   # only want 'two' or 'three'
   criterion = df2['a'].map(lambda x: x.startswith('t'))

   df2[criterion]

   # equivalent but slower
   df2[[x.startswith('t') for x in df2['a']]]

   # Multiple criteria
   df2[criterion & (df2['b'] == 'x')]

With the choice methods :ref:`Selection by Label <indexing.label>`, :ref:`Selection by Position <indexing.integer>` you may select along more than one axis using boolean vectors combined with other indexing expressions.

.. code-block:: python

   df2.loc[criterion & (df2['b'] == 'x'), 'b':'c']

.. _indexing.query:

The :meth:`~pandas.DataFrame.query` Method
------------------------------------------

:class:`~pandas.DataFrame` objects have a :meth:`~pandas.DataFrame.query`
method that allows selection using an expression.

You can get the value of the frame where column ``b`` has values
between the values of columns ``a`` and ``c``. For example:

.. code-block:: python

   n = 10
   df = pd.DataFrame(np.random.rand(n, 3), columns=list('abc'))
   df

   # pure python
   df[(df['a'] < df['b']) & (df['b'] < df['c'])]

   # query
   df.query('(a < b) & (b < c)')

Do the same thing but fall back on a named index if there is no column
with the name ``a``.

.. code-block:: python

   df = pd.DataFrame(np.random.randint(n / 2, size=(n, 2)), columns=list('bc'))
   df.index.name = 'a'
   df
   df.query('a < b and b < c')

If instead you don't want to or cannot name your index, you can use the name
``index`` in your query expression:

.. code-block:: python

   df = pd.DataFrame(np.random.randint(n, size=(n, 2)), columns=list('bc'))
   df
   df.query('index < b < c')

.. note::

   If the name of your index overlaps with a column name, the column name is
   given precedence. For example,

   .. code-block:: python

      df = pd.DataFrame({'a': np.random.randint(5, size=5)})
      df.index.name = 'a'
      df.query('a > 2')  # uses the column 'a', not the index

   You can still use the index in a query expression by using the special
   identifier 'index':

   .. code-block:: python

      df.query('index > 2')

   If for some reason you have a column named ``index``, then you can refer to
   the index as ``ilevel_0`` as well, but at this point you should consider
   renaming your columns to something less ambiguous.


:class:`~pandas.MultiIndex` :meth:`~pandas.DataFrame.query` Syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the levels of a ``DataFrame`` with a
:class:`~pandas.MultiIndex` as if they were columns in the frame:

.. code-block:: python

   n = 10
   colors = np.random.choice(['red', 'green'], size=n)
   foods = np.random.choice(['eggs', 'ham'], size=n)
   colors
   foods

   index = pd.MultiIndex.from_arrays([colors, foods], names=['color', 'food'])
   df = pd.DataFrame(np.random.randn(n, 2), index=index)
   df
   df.query('color == "red"')

If the levels of the ``MultiIndex`` are unnamed, you can refer to them using
special names:

.. code-block:: python

   df.index.names = [None, None]
   df
   df.query('ilevel_0 == "red"')


The convention is ``ilevel_0``, which means "index level 0" for the 0th level
of the ``index``.


:meth:`~pandas.DataFrame.query` Use Cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A use case for :meth:`~pandas.DataFrame.query` is when you have a collection of
:class:`~pandas.DataFrame` objects that have a subset of column names (or index
levels/names) in common. You can pass the same query to both frames *without*
having to specify which frame you're interested in querying

.. code-block:: python

   df = pd.DataFrame(np.random.rand(n, 3), columns=list('abc'))
   df
   df2 = pd.DataFrame(np.random.rand(n + 2, 3), columns=df.columns)
   df2
   expr = '0.0 <= a <= c <= 0.5'
   map(lambda frame: frame.query(expr), [df, df2])

:meth:`~pandas.DataFrame.query` Python versus pandas Syntax Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Full numpy-like syntax:

.. code-block:: python

   df = pd.DataFrame(np.random.randint(n, size=(n, 3)), columns=list('abc'))
   df
   df.query('(a < b) & (b < c)')
   df[(df['a'] < df['b']) & (df['b'] < df['c'])]

Slightly nicer by removing the parentheses (by binding making comparison
operators bind tighter than ``&`` and ``|``).

.. code-block:: python

   df.query('a < b & b < c')

Use English instead of symbols:

.. code-block:: python

   df.query('a < b and b < c')

Pretty close to how you might write it on paper:

.. code-block:: python

   df.query('a < b < c')

The ``in`` and ``not in`` operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:meth:`~pandas.DataFrame.query` also supports special use of Python's ``in`` and
``not in`` comparison operators, providing a succinct syntax for calling the
``isin`` method of a ``Series`` or ``DataFrame``.

.. code-block:: python

   # get all rows where columns "a" and "b" have overlapping values
   df = pd.DataFrame({'a': list('aabbccddeeff'), 'b': list('aaaabbbbcccc'),
                      'c': np.random.randint(5, size=12),
                      'd': np.random.randint(9, size=12)})
   df
   df.query('a in b')

   # How you'd do it in pure Python
   df[df['a'].isin(df['b'])]

   df.query('a not in b')

   # pure Python
   df[~df['a'].isin(df['b'])]


You can combine this with other expressions for very succinct queries:


.. code-block:: python

   # rows where cols a and b have overlapping values
   # and col c's values are less than col d's
   df.query('a in b and c < d')

   # pure Python
   df[df['b'].isin(df['a']) & (df['c'] < df['d'])]


.. note::

   Note that ``in`` and ``not in`` are evaluated in Python, since ``numexpr``
   has no equivalent of this operation. However, **only the** ``in``/``not in``
   **expression itself** is evaluated in vanilla Python. For example, in the
   expression

   .. code-block:: python

      df.query('a in b + c + d')

   ``(b + c + d)`` is evaluated by ``numexpr`` and *then* the ``in``
   operation is evaluated in plain Python. In general, any operations that can
   be evaluated using ``numexpr`` will be.

Special use of the ``==`` operator with ``list`` objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comparing a ``list`` of values to a column using ``==``/``!=`` works similarly
to ``in``/``not in``.

.. code-block:: python

   df.query('b == ["a", "b", "c"]')

   # pure Python
   df[df['b'].isin(["a", "b", "c"])]

   df.query('c == [1, 2]')

   df.query('c != [1, 2]')

   # using in/not in
   df.query('[1, 2] in c')

   df.query('[1, 2] not in c')

   # pure Python
   df[df['c'].isin([1, 2])]

.. _indexing.view_versus_copy:

Returning a view versus a copy
------------------------------

When setting values in a pandas object, care must be taken to avoid what is called
``chained indexing``. Here is an example.

.. code-block:: python

   dfmi = pd.DataFrame([list('abcd'),
                        list('efgh'),
                        list('ijkl'),
                        list('mnop')],
                       columns=pd.MultiIndex.from_product([['one', 'two'],
                                                           ['first', 'second']]))
   dfmi

Compare these two access methods:

.. code-block:: python

   dfmi['one']['second']

.. code-block:: python

   dfmi.loc[:, ('one', 'second')]

These both yield the same results, so which should you use? It is instructive to understand the order
of operations on these and why method 2 (``.loc``) is much preferred over method 1 (chained ``[]``).

``dfmi['one']`` selects the first level of the columns and returns a DataFrame that is singly-indexed.
Then another Python operation ``dfmi_with_one['second']`` selects the series indexed by ``'second'``.
This is indicated by the variable ``dfmi_with_one`` because pandas sees these operations as separate events.
e.g. separate calls to ``__getitem__``, so it has to treat them as linear operations, they happen one after another.

Contrast this to ``df.loc[:,('one','second')]`` which passes a nested tuple of ``(slice(None),('one','second'))`` to a single call to
``__getitem__``. This allows pandas to deal with this as a single entity. Furthermore this order of operations *can* be significantly
faster, and allows one to index *both* axes if so desired.

Why does assignment fail when using chained indexing?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The problem in the previous section is just a performance issue. What's up with
the ``SettingWithCopy`` warning? We don't **usually** throw warnings around when
you do something that might cost a few extra milliseconds!

But it turns out that assigning to the product of chained indexing has
inherently unpredictable results. To see this, think about how the Python
interpreter executes this code:

.. code-block:: python

    value = None

.. code-block:: python

   dfmi.loc[:, ('one', 'second')] = value
   # becomes
   dfmi.loc.__setitem__((slice(None), ('one', 'second')), value)

But this code is handled differently:

.. code-block:: python

   dfmi['one']['second'] = value
   # becomes
   dfmi.__getitem__('one').__setitem__('second', value)

See that ``__getitem__`` in there? Outside of simple cases, it's very hard to
predict whether it will return a view or a copy (it depends on the memory layout
of the array, about which pandas makes no guarantees), and therefore whether
the ``__setitem__`` will modify ``dfmi`` or a temporary object that gets thrown
out immediately afterward. **That's** what ``SettingWithCopy`` is warning you
about!

.. note:: You may be wondering whether we should be concerned about the ``loc``
   property in the first example. But ``dfmi.loc`` is guaranteed to be ``dfmi``
   itself with modified indexing behavior, so ``dfmi.loc.__getitem__`` /
   ``dfmi.loc.__setitem__`` operate on ``dfmi`` directly. Of course,
   ``dfmi.loc.__getitem__(idx)`` may be a view or a copy of ``dfmi``.

Sometimes a ``SettingWithCopy`` warning will arise at times when there's no
obvious chained indexing going on. **These** are the bugs that
``SettingWithCopy`` is designed to catch! Pandas is probably trying to warn you
that you've done this:

.. code-block:: python

   def do_something(df):
       foo = df[['bar', 'baz']]  # Is foo a view? A copy? Nobody knows!
       # ... many lines here ...
       # We don't know whether this will modify df or not!
       foo['quux'] = value
       return foo

Yikes!

.. _indexing.evaluation_order:

Evaluation order matters
~~~~~~~~~~~~~~~~~~~~~~~~

When you use chained indexing, the order and type of the indexing operation
partially determine whether the result is a slice into the original object, or
a copy of the slice.

Pandas has the ``SettingWithCopyWarning`` because assigning to a copy of a
slice is frequently not intentional, but a mistake caused by chained indexing
returning a copy where a slice was expected.

If you would like pandas to be more or less trusting about assignment to a
chained indexing expression, you can set the option
``mode.chained_assignment`` to one of these values:

* ``'warn'``, the default, means a ``SettingWithCopyWarning`` is printed.
* ``'raise'`` means pandas will raise a ``SettingWithCopyException``
  you have to deal with.
* ``None`` will suppress the warnings entirely.

.. code-block:: python

   dfb = pd.DataFrame({'a': ['one', 'one', 'two',
                             'three', 'two', 'one', 'six'],
                       'c': np.arange(7)})

   # This will show the SettingWithCopyWarning
   # but the frame values will be set
   dfb['c'][dfb['a'].str.startswith('o')] = 42

This however is operating on a copy and will not work.

::

   >>> pd.set_option('mode.chained_assignment','warn')
   >>> dfb[dfb['a'].str.startswith('o')]['c'] = 42
   Traceback (most recent call last)
        ...
   SettingWithCopyWarning:
        A value is trying to be set on a copy of a slice from a DataFrame.
        Try using .loc[row_index,col_indexer] = value instead

A chained assignment can also crop up in setting in a mixed dtype frame.

.. note::

   These setting rules apply to all of ``.loc/.iloc``.

This is the correct access method:

.. code-block:: python

   dfc = pd.DataFrame({'A': ['aaa', 'bbb', 'ccc'], 'B': [1, 2, 3]})
   dfc.loc[0, 'A'] = 11
   dfc

This *can* work at times, but it is not guaranteed to, and therefore should be avoided:

.. code-block:: python

   dfc = dfc.copy()
   dfc['A'][0] = 111
   dfc

This will **not** work at all, and so should be avoided:

::

   >>> pd.set_option('mode.chained_assignment','raise')
   >>> dfc.loc[0]['A'] = 1111
   Traceback (most recent call last)
        ...
   SettingWithCopyException:
        A value is trying to be set on a copy of a slice from a DataFrame.
        Try using .loc[row_index,col_indexer] = value instead

.. warning::

   The chained assignment warnings / exceptions are aiming to inform the user of a possibly invalid
   assignment. There may be false positives; situations where a chained assignment is inadvertently
   reported.

.. meta::
    :description lang=en:
        An example of a long HTML page, as is comming in the pandas documentation
        in pydata-sphinx-theme.
