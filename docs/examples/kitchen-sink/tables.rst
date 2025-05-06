..
   Copyright (c) 2021 Pradyun Gedam
   Licensed under Creative Commons Attribution-ShareAlike 4.0 International License
   SPDX-License-Identifier: CC-BY-SA-4.0

======
Tables
======

Grid Tables
-----------

Here's a grid table followed by a simple table:

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+----------+----------+
| body row 5             | Cells may also be     |          |
|                        | empty: ``-->``        |          |
+------------------------+-----------------------+----------+

=====  =====  ======
   Inputs     Output
------------  ------
  A      B    A or B
=====  =====  ======
False  False  False
True   False  True
False  True   True
True   True   True
=====  =====  ======

Giant Tables
^^^^^^^^^^^^

+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+
| Header 1   | Header 2   | Header 3  | Header 1   | Header 2   | Header 3  | Header 1   | Header 2   | Header 3  | Header 1   | Header 2   | Header 3  |
+============+============+===========+============+============+===========+============+============+===========+============+============+===========+
| body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  |
+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+
| body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  |
+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+
| body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  |
+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+
| body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  | body row 1 | column 2   | column 3  |
+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+------------+------------+-----------+

Table containing code
---------------------

==================================== ===========================================
Version                              Installing
==================================== ===========================================
Pradyun's pip fork and installer     .. code-block:: bash

                                        pip install "pip @ git+https://github.com/pradyunsg/pip#20.3.3" "installer @ git+https://github.com/pradyunsg/installer"

PyPI                                 .. code-block:: bash

                                        pip install pip installer

==================================== ===========================================

List Tables
-----------

.. list-table:: List tables can have captions like this one. Fixed widths, *both* header row and header column.
    :widths: 10 5 10 50
    :header-rows: 1
    :stub-columns: 1

    * - List table
      - Header 1
      - Header 2
      - Header 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Link: https://www.sphinx-doc.org/
    * - Stub Row 1
      - Row 1, Col 1
      - Row 1, Col 2
      - Row 1, Col 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Link: https://www.sphinx-doc.org/
    * - Stub Row 2
      - Row 2, Col 1
      - Row 2, Col 2
      - Row 2, Col 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Link: https://www.sphinx-doc.org/
    * - Stub Row 3
      - Row 3, Col 1
      - Row 3, Col 2
      - Row 3, Col 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Link: https://www.sphinx-doc.org/

.. list-table:: A list table with a header *row*, auto-width.
    :header-rows: 1

    * - Header 1
      - Header 2
      - Header 3
      - Header 4 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Row 1, Col 1
      - Row 1, Col 2
      - Row 1, Col 3
      - Row 1, Col 4 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Row 2, Col 1
      - Row 2, Col 2
      - Row 2, Col 3
      - Row 2, Col 4 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Row 3, Col 1
      - Row 3, Col 2
      - Row 3, Col 3
      - Row 3, Col 4 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.

.. list-table:: A list table with a header ("stub") *column*, auto-width.
    :stub-columns: 1

    * - Stub Row 1
      - Row 1, Col 1
      - Row 1, Col 2
      - Row 1, Col 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Stub Row 2
      - Row 2, Col 1
      - Row 2, Col 2
      - Row 2, Col 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Stub Row 3
      - Row 3, Col 1
      - Row 3, Col 2
      - Row 3, Col 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Stub Row 4
      - Row 4, Col 1
      - Row 4, Col 2
      - Row 4, Col 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.

.. list-table:: This is a list table with images in it.

    * - .. figure:: https://picsum.photos/200/200

           This is a short caption for a figure.

      - .. figure:: https://picsum.photos/200/200

           This is a long caption for a figure. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
           Donec porttitor dolor in odio posuere, vitae ornare libero mattis. In lobortis justo vestibulum nibh aliquet, non.
