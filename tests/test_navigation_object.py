import pathlib

import pytest


srcdir = pathlib.Path(__file__).absolute().parent / "examples"


def create_context_nav_assert(expected):
    """
    Sphinx event that is connected to the app to be able to make assertions
    about the `context` while building
    """
    def assert_context_nav_objects(app, pagename, templatename, context, doctree):
        if pagename in expected:
            nav_object = context["get_nav_object"]()
            assert nav_object == expected[pagename]
        elif pagename not in ["genindex", "search"]:
            raise ValueError("page {} not checked".format(pagename))

    return assert_context_nav_objects


@pytest.mark.sphinx(srcdir=srcdir / "test-basic", buildername="html")
def test_navigation_object(app, status, warning):

    expected = dict(
        # only top-level items
        # TODO shouldn't the children actually be included?
        index=[
            {
                "title": "Example page",
                "url": "page.html",
                "active": False,
                "children": [],
            },
            {
                "title": "Example page with sections",
                "url": "page_sections.html",
                "active": False,
                "children": [],
            },
        ],
        page=[
            {
                "title": "Example page",
                "url": "",
                "active": True,
                "children": [
                    {
                        "title": "Subpage 1",
                        "url": "subpage1.html",
                        "active": False,
                        "children": [],
                    },
                    {
                        "title": "Subpage 2",
                        "url": "subpage2.html",
                        "active": False,
                        "children": [],
                    },
                ],
            },
            {
                "title": "Example page with sections",
                "url": "page_sections.html",
                "active": False,
                "children": [],
            },
        ],
        page_sections=[
            {
                "title": "Example page",
                "url": "page.html",
                "active": False,
                "children": [],
            },
            {
                "title": "Example page with sections",
                "url": "",
                "active": True,
                "children": [],
            },
        ],
        subpage1=[
            {
                "title": "Example page",
                "url": "page.html",
                "active": True,
                "children": [
                    {"title": "Subpage 1", "url": "", "active": True, "children": []},
                    {
                        "title": "Subpage 2",
                        "url": "subpage2.html",
                        "active": False,
                        "children": [],
                    },
                ],
            },
            {
                "title": "Example page with sections",
                "url": "page_sections.html",
                "active": False,
                "children": [],
            },
        ],
        subpage2=[
            {
                "title": "Example page",
                "url": "page.html",
                "active": True,
                "children": [
                    {
                        "title": "Subpage 1",
                        "url": "subpage1.html",
                        "active": False,
                        "children": [],
                    },
                    {"title": "Subpage 2", "url": "", "active": True, "children": []},
                ],
            },
            {
                "title": "Example page with sections",
                "url": "page_sections.html",
                "active": False,
                "children": [],
            },
        ],
    )

    app.connect("html-page-context", create_context_nav_assert(expected))
    app.build()
    # path = app.outdir / 'test.tex'
    # assert path.exists() is True
    # content = open(path).read()
