"""This script help checking divergent links.

That is to say, links to the same page,
that have different titles.
"""

import os
import sys
from collections import defaultdict

from bs4 import BeautifulSoup

ignores = ["#", "next", "previous"]


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

    def scan(self, html_content, identifier):
        """Scan given file for html links."""
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Dictionary to store URLs and their corresponding titles

        # Extract all anchor tags
        for a_tag in soup.find_all("a", href=True):
            url = a_tag["href"]
            if url.startswith("#"):
                continue
            content = a_tag.text.strip().lower()
            if content in ignores:
                continue
            if content.split("\n")[0] in ignores:
                continue

            self.links[content].append((url, identifier))

    def duplicates(self):
        """Print potential duplicates."""
        for content, url_pages in self.links.items():
            uniq_url = {u for u, _ in url_pages}
            if len(uniq_url) >= 2:
                print(f"{content} has divergent url:")
                for u, p in url_pages:
                    print(" ", u, "in", p)


# Example usage
data = """
<html>
  <body>
    <a href="https://example.com" title="Example Site">Visit Example</a>
    <a href="https://example.com" title="Example Website">Check Example</a>
    <a href="https://openai.com" title="OpenAI">Visit OpenAI</a>
    <a href="https://openai.com" title="OpenAI">Learn about OpenAI</a>
  </body>
</html>
"""

c = Checker()
# Call the function and print results
# inconsistencies = c.scan(data, "C0")

print(sys.argv)

for file in find_html_files(sys.argv[1]):
    with open(file) as f:
        data = f.read()
    c.scan(data, file)

c.duplicates()
