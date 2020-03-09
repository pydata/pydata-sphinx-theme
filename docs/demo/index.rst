=========
Demo site
=========

This is a simple demonstration site to show off a few visual
and structural elements of the theme. Click the sections on
the left sidebar to see how various elements look on this theme.

.. div:: container

    .. div:: row

        .. div:: col-lg-6 col-md-6 col-sm-6 col-xs-12 d-flex

            .. div:: card text-center intro-card shadow my-5 p-2

                .. image:: ../_static/pandas.svg
                    :class: card-img-top
                    :height: 52px
                    :alt: getting started with pandas action icon

                .. div:: card-body flex-fill

                    .. div:: card-title font-weight-bold text-uppercase

                        Getting started

                    .. div:: card-text

                    New to *pandas*? Check out the getting started guides. They
                    contain an introduction to *pandas'* main concepts and links to
                    additional tutorials.

        .. div:: col-lg-6 col-md-6 col-sm-6 col-xs-12 d-flex

            .. div:: card text-center intro-card shadow my-5 p-2

                .. image:: ../_static/pandas.svg
                    :class: card-img-top
                    :height: 52px
                    :alt: pandas user guide action icon

                .. div:: card-body flex-fill

                    .. div:: card-title font-weight-bold text-uppercase

                        User Guide

                    .. div:: card-text

                    The user guide provides in-depth information on the key concepts
                    of pandas with useful background information and explanation.

.. toctree::
    :maxdepth: 2
    :caption: Demo Documentation

    structure
    demo
    api
    lists_tables
    markdown
    example_pandas

.. toctree::
    :maxdepth: 3
    :numbered:
    :caption: This is an incredibly long caption for a long menu

    long
