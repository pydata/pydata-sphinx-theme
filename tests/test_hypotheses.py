""" property-based testing for for a sphinx site
"""
from pathlib import Path
import tempfile
from hypothesis import given, settings, HealthCheck, strategies as st
from sphinx.testing.path import path as sphinx_path

a_kind = st.sampled_from(["raw", "navbar", "sidebar"])
a_depth = st.one_of(st.none(), st.integers(min_value=0))
a_navbar_align = st.one_of(st.none(), st.sampled_from(["content", "left", "right"]))
a_caption = st.one_of(st.none(), st.text(min_size=1))

# TODO: fill out rest of schema
# a_use_edit_page_button = st.one_of(st.none(), st.booleans())

# TODO: fill out rest of set
# a_page_names = st.sets(st.text(min_size=1).filter(lambda x: x != "index"))

ALWAYS_LINES = [
    # because we are testing this site
    "html_theme = 'pydata_sphinx_theme'",
]


@st.composite
def a_conf_py(
    draw,
    show_toc_level=st.integers(min_value=0),
    # use_edit_page_button=a_use_edit_page_button,
    navbar_align=a_navbar_align,
):
    """Generates a (hopefully) valid conf.py"""
    lines = []

    html_theme_options = {}

    stl = draw(show_toc_level)
    if stl:
        html_theme_options["show_toc_level"] = stl

    # TODO: fill out rest of schema
    # uepb = draw(use_edit_page_button)
    # if uepb is not None:
    #     html_theme_options["use_edit_page_button"] = uepb

    na = draw(a_navbar_align)
    if na is not None:
        html_theme_options["navbar_align"] = na

    if html_theme_options:
        lines += [f"html_theme_options = {html_theme_options}"]

    return lines


@st.composite
def a_toctree_header(draw, maxdepth=a_depth, caption=a_caption):
    """Generate a toctree directive with options"""
    lines = ["", ".. toctree::"]

    md = draw(maxdepth)
    if md is not None:
        lines += [f"    :maxdepth: {md}"]

    c = draw(caption)
    if caption is not None:
        lines += [f"    :caption: {c}"]

    return [*lines, ""]


@st.composite
def a_index_rst(
    draw,
    name=st.text(min_size=1),
    num_tocs=st.integers(min_value=0, max_value=100),
    toctree_header=a_toctree_header(),
):
    """Generates an index.rst"""
    n = draw(name)

    head = "=" * len(n)
    lines = [head, n, head, ""]

    for i in range(draw(num_tocs)):
        lines += draw(toctree_header)

    return lines


@st.composite
def a_site(draw, index_rst=a_index_rst()):
    """Generates a site with an index and a number of other files (keyed by name)"""
    ir = draw(index_rst)
    return (ir, {})


@settings(
    suppress_health_check=[
        # TODO: this _might_ be hiding problems
        HealthCheck.function_scoped_fixture
    ],
    # nothing for it, app.build is slow unless we figure out a way to keep in RAM
    deadline=None,
)
@given(conf_py=a_conf_py(), site=a_site())
def test_a_valid_site_builds(make_app, conf_py, site):
    """Does a properly-configured site build without error?

    This only tests whether the site _builds_, not whether it looks rights
    """
    index_rst, pages = site
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "conf.py").write_text("\n\n".join([*ALWAYS_LINES, *conf_py]))
        (tdp / "index.rst").write_text("\n".join(index_rst))
        build_html = tdp / "_build/html"
        app = make_app(srcdir=sphinx_path(tdp))
        app.build()
        generated = [*build_html.rglob("*.html")]
        assert len(generated) > 0
        assert (build_html / "index.html").exists()
