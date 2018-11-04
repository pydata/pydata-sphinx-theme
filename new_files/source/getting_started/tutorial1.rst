.. _tutorial1:

================================================
pandas tutorial - Part I: Introduction to pandas
================================================

Welcome to pandas. In this first tutorial you will learn about the basic
functionality that pandas provides.

Loading data
------------

pandas can load data from a large number of formats, including SQL databases,
CSV, JSON, Parquet or HTML files, or even the system clipboard, among others.

We will start by loading some data about animals from a CSV file:

.. ipython:: python

   import pandas

   animals = pandas.read_csv('data/animals.csv')

This will save in the variable `animals` a table (in the pandas terminology
a :class:`DataFrame`) with the contents of the CSV file.

The function :func:`read_csv` supports a large number of parameters, to
control how the data is load. For example, we can specify that the column
delimiter is a semi-colon (the default is comma), by setting ``sep=';'``.
Or in files without a header, we can set the column names with
``header=['name', 'class', ...]``. For the list of all accepted
parameters, and extended documentation, the API reference can be checked:
:ref:`read_csv`.

All pandas functions to load from files support automatically downloading
the files, and automatically uncompressing them. For example, if our file
was compressed with zip, and available in a website, we could load it by
simply using:

.. ipython:: python

   animals = pandas.read_csv('https://pandas.pydata.org/docs/data/animals.csv.zip')

To load from a different format, like JSON, the syntax is very similar:

.. ipython:: python

   countries = pandas.read_json('data/countries.json', orient='records')

Like :func:`read_csv` and all pandas functions to load data, :func:`read_json`
also accepts parameters to control how the data is loaded, and to specify
its format. In this case ``orient='records'`` tells that the expected format
of the JSON file is a list of dictionaries, where the keys are the column
names, and the values are the values.

In some cases, it can also be useful to construct the :class:`DataFrame`
directly from Python object. This can easily be accomplished with the
:class:`DataFrame` constructor, which accepts different formats as input,
like a `dict` or a `list` of `tuple`, for example:

.. ipython:: python

   gender = pandas.DataFrame({'code': ['F', 'M', 'O'],
                              'name': ['Female', 'Male', 'Other']})

More information on loading data can be found in the :ref:`IO Tools <io>`
page. Including the list of available formats.

Viewing data
------------

One thing that we may want to do with our :class:`DataFrame` is to visualize
its content.

By just displaying the content of the variable with the :class:`DataFrame` we
can see a preview of the data. In many cases, the number of rows is so long
that it may be worth displaying only a subset. We can display the first 5
rows by using :meth:`DataFrame.head`:

.. ipython:: python

   animals.head()

We can also print the last rows by using :meth:`DataFrame.tail`, and we can
change the number of rows to display by changing the parameter `n`:

.. ipython:: python

   animals.tail(3)

To better understand our data, specially when it is large, and is not easy
to display all the rows, we can use :meth:`DataFrame.info` (which shows a
summary of the columns) and :meth:`DataFrame.describe` (which shows the
basic statistics, mainly of the numerical columns).

.. ipython:: python

   animals.info()
   animals.describe()

In some cases, it can be useful to display the data transposed. So, the
columns become rows, and vice-versa. This can be done with the property
:meth:`DataFrame.T` (an alias for :meth:`DataFrame.transpose`):

.. ipython:: python

   animals.head(3).T
