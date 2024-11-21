"""This script help checking inconsistent links.

That is to say, links that have the same title but go to different places.
This is useful for screen-reader and accessibility devices, where the user may
say "Go to X", but if there are 2 links named "X" this creates ambiguity.


Example (links that have the same name, but different URL):

   We have a JavaScript <a href="javascript.html">API</a> and
   a Python <a href="python.html">API</a>.

How to fix (give the links different names):

   We have a <a href="javascript.html">JavaScript API</a> and
   a <a href="python.html">Python API</a>.
"""

import os
import sys

from collections import defaultdict
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from rich import print


# when looking at inconsistent links across pages,
# a number of text is recurrent and appear on many pages.
# So we'll ignore these.

ignores = [
    "#",
    "next",
    "previous",
    "[source]",
    "edit on github",
    "[docs]",
    "read more ...",
    "show source",
    "module",
]


def find_html_files(folder_path):
    """Find all html files in given folder."""
    html_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files


class Checker:
    """Link checker."""

    links: dict[str, list]

    def __init__(self):
        self.links = defaultdict(list)

    def scan(self, html_content, file_path):
        """Scan given file for html links."""
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Dictionary to store URLs and their corresponding titles

        # Extract all anchor tags
        for a_tag in soup.find_all("a", href=True):
            url = a_tag["href"]

            # These are usually link into the same page ("see below", or even
            # header anchors  we thus exclude those.
            if url.startswith("#"):
                continue
            content = a_tag.text.strip().lower()
            if content in ignores:
                continue
            # Some links are "$Title\nNext", or "$Title\nprev", so we only
            # want to look at what is before the `\n`
            if content.split("\n")[0] in ignores:
                continue

            fullurl = urljoin(file_path, url)
            self.links[content].append((fullurl, file_path))

    def duplicates(self):
        """Print potential duplicates."""
        for content, url_pages in self.links.items():
            uniq_url = {u for u, _ in url_pages}
            if len(uniq_url) >= 2:
                print(
                    f"The link text [red]{content!r}[/red] appears {len(url_pages)} "
                    f"times and links to {len(uniq_url)} different URLs, "
                    f"on the following pages:"
                )
                dct = defaultdict(list)
                for u, p in url_pages:
                    dct[u].append(p)
                for u, ps in dct.items():
                    print(f"  [blue]{u}[/blue] in")
                    for p in set(ps):
                        print(f"    [green]{p}[/green]")


if len(sys.argv) == 3 and sys.argv[2] == "--all":
    c = Checker()

    for file in find_html_files(sys.argv[1]):
        with open(file) as f:
            data = f.read()
        c.scan(data, file)

    c.duplicates()
elif len(sys.argv) == 2:
    for file in find_html_files(sys.argv[1]):
        with open(file) as f:
            data = f.read()
        c = Checker()
        c.scan(data, file)
        c.duplicates()
else:
    print(
        """
Check page-wise link consistency
(links with the same name on the same page should go to the same URL)

      python tools/divergent_links.py docs/_build/html/

Check site-wide link consistency
(links with the same name across all pages should go the same URL)

      python tools/divergent_links.py docs/_build/html/ --all

"""
    )
    sys.exit(1)
