# Galleries and the `gallery-grid` directive

There are a few places where we use `sphinx-design` to generate "galleries" of grids with structured text and images.
We've created a little Sphinx directive to make it easier to repeat this process in our documentation and to avoid repeating ourselves too much.
It is located in the `docs/scripts/` folder in a dedicated module, and re-used throughout our documentation.

## The example gallery

This theme's documentation contains a gallery of sites that use this theme for their documentation.
The images are automatically generated during ReadTheDocs builds, but are **not** automatically generated on local or test builds (to save time).

If you build the documentation locally without first generating these images you may get Sphinx warnings or errors, but this should be fine as long as the images build on ReadTheDocs tests.

### Download gallery images locally

If you'd like to build these images locally to preview in the theme, follow these steps:

1. Install [playwright](https://playwright.dev/python/) and the Chromium browser add-on:

   ```
   $ pip install playwright
   $ playwright install chromium
   ```

2. Execute the gallery generation script from the repository root:

   ```
   $ python ./docs/scripts/generate_gallery_images.py
   ```

:::{note}
The newly generated images will be pushed to the distant repository.
:::
