Upgrade to bootstrap 5
======================

Since *v0.13*, ``pydata-sphinx-theme`` has moved from Bootstrap 4 to bootstrap 5. This documentation will guide you through the changes we made and the one you should take care of in your existing documentation.

Dropping **JQuery**
-------------------

Bootstrap Dropped **jQuery** dependency and rewrote plugins to be in regular JavaScript. Note that Sphinx *v6* will do the same (https://github.com/sphinx-doc/sphinx/issues/10070). As a consequence, we also rewrote all our javascript to only use vanilla **JavaScript**. Any documentation relying on **JQuery** in their ``custom.js`` will need to rewrite it or specifically importy **JQuery**.

Breaking changes
----------------

If your documentation was using a ``custom.css`` and/or a ``custom.js``, please pay attention to this migration items.

.. tip::

    All the changes from *v4* to *v5* are listed in their documentation: https://getbootstrap.com/docs/5.0/migration/. We will only list the one the have consequences on some of ``pydata-sphinx-theme`` components.

-   Media query mixins parameters have changed for a more logical approach.
    -   ``media-breakpoint-down()`` uses the breakpoint itself instead of the next breakpoint (e.g., ``media-breakpoint-down(lg)`` instead of ``media-breakpoint-down(md)`` targets viewports smaller than lg).
    -   Similarly, the second parameter in ``media-breakpoint-between()`` also uses the breakpoint itself instead of the next breakpoint (e.g., ``media-between(sm, lg)`` instead of ``media-breakpoint-between(sm, md)`` targets viewports between sm and lg).

-   ``box-shadow`` mixins now allow ``null`` values and drop ``none`` from multiple arguments.

-   Nested tables do not inherit styles anymore.

-   ``.thead-light`` and ``.thead-dark`` are dropped in favor of the ``.table-*`` variant classes which can be used for all table elements (``thead``, ``tbody``, ``tfoot``, ``tr``, ``th`` and ``td``).

-   Dropped ``.text-justify`` class. See https://github.com/twbs/bootstrap/pull/29793

-   Renamed several utilities to use logical property names instead of directional names with the addition of RTL support:

    -   Renamed ``.left-*`` and ``.right-*`` to ``.start-*`` and ``.end-*``.
    -   Renamed ``.float-left`` and ``.float-right`` to ``.float-start`` and ``.float-end``.
    -   Renamed ``.border-left`` and ``.border-right`` to ``.border-start`` and ``.border-end``.
    -   Renamed ``.rounded-left`` and ``.rounded-right`` to ``.rounded-start`` and ``.rounded-end``.
    -   Renamed ``.ml-*`` and ``.mr-*`` to ``.ms-*`` and ``.me-*``.
    -   Renamed ``.pl-*`` and ``.pr-*`` to ``.ps-*`` and ``.pe-*``.
    -   Renamed ``.text-left`` and ``.text-right`` to ``.text-start`` and ``.text-end``.

-   Data attributes for all JavaScript plugins are now namespaced to help distinguish Bootstrap functionality from third parties and your own code. For example, we use ``data-bs-toggle`` instead of ``data-toggle``.
