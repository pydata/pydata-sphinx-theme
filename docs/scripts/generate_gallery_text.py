"""
Use playwright to build a gallery of website using this theme
"""

from pathlib import Path
import json
from shutil import copy
from playwright.sync_api import sync_playwright, TimeoutError
from rich.progress import track
from rich import print
from textwrap import indent, dedent


def regenerate_gallery():
    """
    Regenerate the gallery of snapshots from external websites.

    This function should only be triggered in RTD builds as it increases the build
    time by 30-60s. Developers can still execute this function from time to time to
    populate the repository with updated files.
    """

    gallery_directive = dedent(
        """
    .. grid:: 1 1 1 2
       :gutter: 3
    """
    ).strip()

    gallery_item_template = dedent(
        """
    .. grid-item-card:: {name}
       :img-bottom: {path_image}
       :link: {website}"""
    )

    # get the existing folders path
    _template_dir = Path(__file__).parents[1] / "_templates"
    demo_dir = Path(__file__).parents[1] / "demo"
    _static_dir = Path(__file__).parents[1] / "_static"

    # update the gallery file with a new empty one
    src = _template_dir / "gallery.rst"
    dst = demo_dir / "gallery.rst"
    print(f"Using gallery template from: {src}")

    # create the static gallery folder where we'll put the gallery source files
    gallery_dir = _static_dir / "gallery"
    gallery_dir.mkdir(exist_ok=True)

    # load gallery data
    gallery_items = json.loads((_template_dir / "gallery.json").read_text())
    image_404 = _static_dir / "404.png"

    gallery_directive_items = []
    with sync_playwright() as p:
        # Generate our browser to visit pages and generate images
        for ii in range(3):
            try:
                browser = p.chromium.launch()
                break
            except TimeoutError:
                print(f"Browser start timed out. Trying again (attempt {ii+2}/3)")
        page = browser.new_page()

        for item in track(gallery_items, description="Generating screenshots..."):
            item["id"] = item["name"].lower().replace(" ", "_")
            screenshot = gallery_dir / f"{item['id']}.png"

            # Visit the page and take a screenshot
            for ii in range(3):
                try:
                    page.goto(item["website"])
                    page.screenshot(path=screenshot)
                    break
                except TimeoutError:
                    print(f"Page visit start timed out for: {item['website']}")
                    print(f"Trying again (attempt {ii+2}/3)")

            # copy the 404 only if the screenshot file was not manually
            # generated by a maintainer
            if not screenshot.is_file():
                print(f"Could not generate screenshot for {item['name']}, using 404.")
                copy(image_404, screenshot)

            # remove non use information maybe remove this line once the json
            # will be updated
            item.pop("repo", None)

            # add the new gallery item to the gallery file
            item["path_image"] = Path("..") / "_static" / "gallery" / f"{item.pop('id')}.png"
            gallery_directive_items.append(f"\n{gallery_item_template.format(**item)}")

        # Clean up the browser since we no longer need it
        browser.close()

    # Turn our gallery items into a string and add to our directive
    gallery_directive_items = indent("\n".join(gallery_directive_items), "   ")
    gallery_directive += gallery_directive_items

    dst.write_text(src.read_text().format(gallery_directive=gallery_directive))
    print(f"Finished generating gallery at: {dst}")


if __name__ == "__main__":
    regenerate_gallery()
