"""
Use playwright to build a gallery of website using this theme
"""

from pathlib import Path
import json
from shutil import copy
from playwright.sync_api import sync_playwright, TimeoutError


def regenerate_gallery():
    """
    Regenerate the gallery files from the current version of their website
    This function should only be triggered in RDT build as it's increasing the building
    time by 30-60s. Developers can still execute this function from time to time to
    populate the repository with updated files
    """

    # get the existing folders path
    _template_dir = Path(__file__).parents[1] / "_templates"
    user_guide_dir = Path(__file__).parents[1] / "user_guide"
    _static_dir = Path(__file__).parents[1] / "_static"

    # update the gallery file with a new empty one
    src = _template_dir / "gallery.rst"
    dst = user_guide_dir / "gallery.rst"
    copy(src, dst)

    # hydrate the gallery with new images
    site_content = (_template_dir / "gallery_item.rst").read_text()
    gallery_items = json.loads((_template_dir / "gallery.json").read_text())
    image_404 = _static_dir / "404.png"

    with dst.open("a") as f, sync_playwright() as p:
        for item in gallery_items:

            item["id"] = item["name"].lower().replace(" ", "_")
            screenshot = _static_dir / f"gallery/{item['id']}.png"

            try:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(item["website"])
                page.screenshot(path=screenshot)
                browser.close()

            except TimeoutError:
                copy(image_404, screenshot)

            # remove non use information maybe remove this line once the json
            # will be updated
            item.pop("repo", None)

            # add the new gallery item to the gallery file
            f.write(site_content.format(**item))


if __name__ == "__main__":
    regenerate_gallery()
