from urllib.request import urlopen
from pathlib import Path

EXTRA_MESSAGE = """\
.. note::

   The Kitchen Sink was generated from the `Sphinx Themes website <https://sphinx-themes.org/>`_, a community-supported showcase of themes for `Sphinx <https://sphinx-doc.org>`_.
   Check it out to see other great themes.

   .. button-link:: https://sphinx-themes.org
      :color: primary

      Go to Sphinx Themes
"""  # noqa

kitchen_sink_files = [
    "admonitions.rst",
    "api.rst",
    "blocks.rst",
    "generic.rst",
    "images.rst",
    "index.rst",
    "lists.rst",
    "really-long.rst",
    "structure.rst",
    "tables.rst",
    "typography.rst",
]
path_sink = Path(__file__).parent.parent / "examples" / "kitchen-sink"
for ifile in kitchen_sink_files:
    print(f"Reading {ifile}...")
    url = f"https://github.com/sphinx-themes/sphinx-themes.org/raw/master/sample-docs/kitchen-sink/{ifile}"  # noqa
    text = urlopen(url).read().decode()
    # The sphinx-themes docs expect Furo to be installed, so we overwrite w/ PST
    text = text.replace("src/furo", "src/pydata_sphinx_theme")
    text = text.replace(":any:`sphinx.ext.autodoc`", "``sphinx.ext.autodoc``")
    # Add introductory message directing people to Sphinx Themes
    if "index" in ifile:
        text = text.replace("============", "============\n\n" + EXTRA_MESSAGE)
    (path_sink / f"{ifile}").write_text(text)

print(f"Finished updating {len(kitchen_sink_files)} files...")
