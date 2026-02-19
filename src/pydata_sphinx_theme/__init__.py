"""Bootstrap-based sphinx theme from the PyData community."""

import json

from functools import partial
from pathlib import Path
from typing import Dict
from urllib.parse import urlparse

import requests

from requests.exceptions import ConnectionError, HTTPError, RetryError
from sphinx.application import Sphinx
from sphinx.builders.dirhtml import DirectoryHTMLBuilder
from sphinx.errors import ExtensionError

from . import edit_this_page, logo, pygments, short_link, toctree, translator, utils


__version__ = "0.16.2dev0"


def update_config(app):
    """Update config with new default values and handle deprecated keys."""
    # By the time `builder-inited` happens, `app.builder.theme_options` already exists.
    # At this point, modifying app.config.html_theme_options will NOT update the
    # page's HTML context (e.g. in jinja, `theme_keyword`).
    # To do this, you must manually modify `app.builder.theme_options`.
    theme_options = utils.get_theme_options_dict(app)
    warning = partial(utils.maybe_warn, app)

    # TODO: DEPRECATE after v1.0
    themes = ["light", "dark"]
    for theme in themes:
        if style := theme_options.get(f"pygment_{theme}_style"):
            theme_options[f"pygments_{theme}_style"] = style
            warning(
                f'The parameter "pygment_{theme}_style" was renamed to '
                f'"pygments_{theme}_style" (note the "s" on "pygments").'
            )

    # Validate icon links
    if not isinstance(theme_options.get("icon_links", []), list):
        raise ExtensionError(
            "`icon_links` must be a list of dictionaries, you provided "
            f"type {type(theme_options.get('icon_links'))}."
            "If you wish to disable this feature, either do not provide "
            "a value (leave undefined), or set to an empty list."
        )

    # Set the anchor link default to be # if the user hasn't provided their own
    if not utils.config_provided_by_user(app, "html_permalinks_icon"):
        app.config.html_permalinks_icon = "#"

    # check the validity of the theme switcher file
    is_dict = isinstance(theme_options.get("switcher"), dict)
    should_test = theme_options.get("check_switcher", True)
    if is_dict and should_test:
        theme_switcher = theme_options.get("switcher")

        # raise an error if one of these compulsory keys is missing
        json_url = theme_switcher["json_url"]
        theme_switcher["version_match"]

        # try to read the json file. If it's a url we use request,
        # else we simply read the local file from the source directory
        # display a log warning if the file cannot be reached
        reading_error = None
        if urlparse(json_url).scheme in ["http", "https"]:
            try:
                request = requests.get(json_url)
                request.raise_for_status()
                content = request.text
            except (ConnectionError, HTTPError, RetryError) as e:
                reading_error = repr(e)
        else:
            try:
                content = Path(app.srcdir, json_url).read_text()
            except FileNotFoundError as e:
                reading_error = repr(e)

        if reading_error is not None:
            warning(
                f'The version switcher "{json_url}" file cannot be read due to '
                f"the following error:\n{reading_error}"
            )
        else:
            # check that the json file is not illformed,
            # throw a warning if the file is ill formed and an error if it's not json
            switcher_content = json.loads(content)
            missing_url = any(["url" not in e for e in switcher_content])
            missing_version = any(["version" not in e for e in switcher_content])
            if missing_url or missing_version:
                warning(
                    f'The version switcher "{json_url}" file is malformed; '
                    'at least one of the items is missing the "url" or "version" key'
                )

    # Add an analytics ID to the site if provided
    analytics = theme_options.get("analytics", {})
    if analytics:
        # Plausible analytics
        plausible_domain = analytics.get("plausible_analytics_domain")
        plausible_url = analytics.get("plausible_analytics_url")

        # Ref: https://plausible.io/docs/plausible-script
        if plausible_domain and plausible_url:
            kwargs = {
                "loading_method": "defer",
                "data-domain": plausible_domain,
                "filename": plausible_url,
            }
            app.add_js_file(**kwargs)

        # Google Analytics
        gid = analytics.get("google_analytics_id")
        if gid:
            gid_js_path = f"https://www.googletagmanager.com/gtag/js?id={gid}"
            gid_script = f"""
                window.dataLayer = window.dataLayer || [];
                function gtag(){{ dataLayer.push(arguments); }}
                gtag('consent', 'default', {{
                    'ad_storage': 'denied',
                    'ad_user_data': 'denied',
                    'ad_personalization': 'denied',
                    'analytics_storage': 'denied'
                }});
                gtag('js', new Date());
                gtag('config', '{gid}');
            """

            # Link the JS files
            app.add_js_file(gid_js_path, loading_method="async")
            app.add_js_file(None, body=gid_script)

    # Update ABlog configuration default if present
    fa_provided = utils.config_provided_by_user(app, "fontawesome_included")
    if "ablog" in app.config.extensions and not fa_provided:
        app.config.fontawesome_included = True

    # Handle icon link shortcuts
    shortcuts = [
        ("twitter_url", "fa-brands fa-square-twitter", "Twitter", "fontawesome"),
        ("bitbucket_url", "fa-brands fa-bitbucket", "Bitbucket", "fontawesome"),
        ("gitlab_url", "fa-brands fa-square-gitlab", "GitLab", "fontawesome"),
        ("github_url", "fa-brands fa-square-github", "GitHub", "fontawesome"),
        (
            "forgejo_url",
            r"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 212 212'%3E%3Cstyle%3Ecircle,path%7Bfill:none;stroke:%23000;stroke-width:15%7Dpath%7Bstroke-width:25%7D.orange%7Bstroke:%23f60%7D.red%7Bstroke:%23d40000%7D%3C/style%3E%3Cg transform='translate(6 6)'%3E%3Cpath d='M58 168V70a50 50 0 0 1 50-50h20' class='orange'/%3E%3Cpath d='M58 168v-30a50 50 0 0 1 50-50h20' class='red'/%3E%3Ccircle cx='142' cy='20' r='18' class='orange'/%3E%3Ccircle cx='142' cy='88' r='18' class='red'/%3E%3Ccircle cx='58' cy='180' r='18' class='red'/%3E%3C/g%3E%3C/svg%3E",
            "Forgejo",
            "local",
        ),
        (
            "gitea_url",
            r"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 640'%3E%3Cpath fill='%23fff' d='m395.9 484.2-126.9-61c-12.5-6-17.9-21.2-11.8-33.8l61-126.9c6-12.5 21.2-17.9 33.8-11.8 17.2 8.3 27.1 13 27.1 13l-.1-109.2 16.7-.1.1 117.1s57.4 24.2 83.1 40.1c3.7 2.3 10.2 6.8 12.9 14.4 2.1 6.1 2 13.1-1 19.3l-61 126.9c-6.2 12.7-21.4 18.1-33.9 12z'/%3E%3Cg fill='%23609926'%3E%3Cpath d='M622.7 149.8c-4.1-4.1-9.6-4-9.6-4s-117.2 6.6-177.9 8c-13.3.3-26.5.6-39.6.7v117.2c-5.5-2.6-11.1-5.3-16.6-7.9 0-36.4-.1-109.2-.1-109.2-29 .4-89.2-2.2-89.2-2.2s-141.4-7.1-156.8-8.5c-9.8-.6-22.5-2.1-39 1.5-8.7 1.8-33.5 7.4-53.8 26.9C-4.9 212.4 6.6 276.2 8 285.8c1.7 11.7 6.9 44.2 31.7 72.5 45.8 56.1 144.4 54.8 144.4 54.8s12.1 28.9 30.6 55.5c25 33.1 50.7 58.9 75.7 62 63 0 188.9-.1 188.9-.1s12 .1 28.3-10.3c14-8.5 26.5-23.4 26.5-23.4S547 483 565 451.5c5.5-9.7 10.1-19.1 14.1-28 0 0 55.2-117.1 55.2-231.1-1.1-34.5-9.6-40.6-11.6-42.6zM125.6 353.9c-25.9-8.5-36.9-18.7-36.9-18.7S69.6 321.8 60 295.4c-16.5-44.2-1.4-71.2-1.4-71.2s8.4-22.5 38.5-30c13.8-3.7 31-3.1 31-3.1s7.1 59.4 15.7 94.2c7.2 29.2 24.8 77.7 24.8 77.7s-26.1-3.1-43-9.1zm300.3 107.6s-6.1 14.5-19.6 15.4c-5.8.4-10.3-1.2-10.3-1.2s-.3-.1-5.3-2.1l-112.9-55s-10.9-5.7-12.8-15.6c-2.2-8.1 2.7-18.1 2.7-18.1L322 273s4.8-9.7 12.2-13c.6-.3 2.3-1 4.5-1.5 8.1-2.1 18 2.8 18 2.8L467.4 315s12.6 5.7 15.3 16.2c1.9 7.4-.5 14-1.8 17.2-6.3 15.4-55 113.1-55 113.1z'/%3E%3Cpath d='M326.8 380.1c-8.2.1-15.4 5.8-17.3 13.8-1.9 8 2 16.3 9.1 20 7.7 4 17.5 1.8 22.7-5.4 5.1-7.1 4.3-16.9-1.8-23.1l24-49.1c1.5.1 3.7.2 6.2-.5 4.1-.9 7.1-3.6 7.1-3.6 4.2 1.8 8.6 3.8 13.2 6.1 4.8 2.4 9.3 4.9 13.4 7.3.9.5 1.8 1.1 2.8 1.9 1.6 1.3 3.4 3.1 4.7 5.5 1.9 5.5-1.9 14.9-1.9 14.9-2.3 7.6-18.4 40.6-18.4 40.6-8.1-.2-15.3 5-17.7 12.5-2.6 8.1 1.1 17.3 8.9 21.3 7.8 4 17.4 1.7 22.5-5.3 5-6.8 4.6-16.3-1.1-22.6 1.9-3.7 3.7-7.4 5.6-11.3 5-10.4 13.5-30.4 13.5-30.4.9-1.7 5.7-10.3 2.7-21.3-2.5-11.4-12.6-16.7-12.6-16.7-12.2-7.9-29.2-15.2-29.2-15.2s0-4.1-1.1-7.1c-1.1-3.1-2.8-5.1-3.9-6.3 4.7-9.7 9.4-19.3 14.1-29-4.1-2-8.1-4-12.2-6.1-4.8 9.8-9.7 19.7-14.5 29.5-6.7-.1-12.9 3.5-16.1 9.4-3.4 6.3-2.7 14.1 1.9 19.8l-24.6 50.4z'/%3E%3C/g%3E%3C/svg%3E",
            "Gitea",
            "local",
        ),
    ]
    # Add extra icon links entries if there were shortcuts present
    # TODO: Deprecate this at some point in the future?
    icon_links = theme_options.get("icon_links", [])
    for url, icon, name, icon_type in shortcuts:
        if theme_options.get(url):
            # This defaults to an empty list so we can always insert
            icon_links.insert(
                0,
                {
                    "url": theme_options.get(url),
                    "icon": icon,
                    "name": name,
                    "type": icon_type,
                },
            )
            icon_links[0] = adjust_known_instances(icon_links[0])
    theme_options["icon_links"] = icon_links

    # Prepare the logo config dictionary
    theme_logo = theme_options.get("logo")
    if not theme_logo:
        # In case theme_logo is an empty string
        theme_logo = {}
    if not isinstance(theme_logo, dict):
        raise ValueError(f"Incorrect logo config type: {type(theme_logo)}")
    theme_logo_link = theme_options.get("theme_logo_link")
    if theme_logo_link:
        theme_logo["link"] = theme_logo_link
    theme_options["logo"] = theme_logo


def update_and_remove_templates(
    app: Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    """Update template names and assets for page build."""
    # Allow for more flexibility in template names
    template_sections = [
        "theme_navbar_start",
        "theme_navbar_center",
        "theme_navbar_persistent",
        "theme_navbar_end",
        "theme_article_header_start",
        "theme_article_header_end",
        "theme_article_footer_items",
        "theme_content_footer_items",
        "theme_footer_start",
        "theme_footer_center",
        "theme_footer_end",
        "theme_primary_sidebar_end",
        "sidebars",
    ]
    for section in template_sections:
        if context.get(section):
            context[section] = utils._update_and_remove_templates(
                app=app,
                context=context,
                templates=context.get(section, []),
                section=section,
                templates_skip_empty_check=["sidebar-nav-bs.html", "navbar-nav.html"],
            )

    # Remove a duplicate entry of the theme CSS. This is because it is in both:
    # - theme.conf
    # - manually linked in `webpack-macros.html`
    if "css_files" in context:
        theme_css_name = "_static/styles/pydata-sphinx-theme.css"
        for i in range(len(context["css_files"])):
            asset = context["css_files"][i]
            # TODO: eventually the contents of context['css_files'] etc should probably
            # only be _CascadingStyleSheet etc. For now, assume mixed with strings.
            asset_path = getattr(asset, "filename", str(asset))
            if asset_path == theme_css_name:
                del context["css_files"][i]
                break
    # Add links for favicons in the topbar
    for favicon in context.get("theme_favicons", []):
        icon_type = Path(favicon["href"]).suffix.strip(".")
        opts = {
            "rel": favicon.get("rel", "icon"),
            "sizes": favicon.get("sizes", "16x16"),
            "type": f"image/{icon_type}",
        }
        if "color" in favicon:
            opts["color"] = favicon["color"]
        # Sphinx will auto-resolve href if it's a local file
        app.add_css_file(favicon["href"], **opts)

    # Add metadata to DOCUMENTATION_OPTIONS so that we can re-use later
    # Pagename to current page
    app.add_js_file(None, body=f"DOCUMENTATION_OPTIONS.pagename = '{pagename}';")
    if isinstance(context.get("theme_switcher"), dict):
        theme_switcher = context["theme_switcher"]
        json_url = theme_switcher["json_url"]
        version_match = theme_switcher["version_match"]

        # Add variables to our JavaScript for re-use in our main JS script
        js = f"""
        DOCUMENTATION_OPTIONS.theme_version = '{__version__}';
        DOCUMENTATION_OPTIONS.theme_switcher_json_url = '{json_url}';
        DOCUMENTATION_OPTIONS.theme_switcher_version_match = '{version_match}';
        DOCUMENTATION_OPTIONS.show_version_warning_banner =
            {str(context["theme_show_version_warning_banner"]).lower()};
        """
        app.add_js_file(None, body=js)

    # Specify whether search-as-you-type should be used or not.
    search_as_you_type = str(context["theme_search_as_you_type"]).lower()
    app.add_js_file(
        None, body=f"DOCUMENTATION_OPTIONS.search_as_you_type = {search_as_you_type};"
    )

    # Update version number for the "made with version..." component
    context["theme_version"] = __version__


def _fix_canonical_url(
    app: Sphinx, pagename: str, templatename: str, context: dict, doctree
) -> None:
    """Fix the canonical URL when using the dirhtml builder.

    Sphinx builds a canonical URL if ``html_baseurl`` config is set. However,
    it builds a URL ending with ".html" when using the dirhtml builder, which is
    incorrect. Detect this and generate the correct URL for each page.

    Workaround for https://github.com/sphinx-doc/sphinx/issues/9730; can be removed
    when that is fixed, released, and available in our minimum supported Sphinx version.
    """
    if (
        not app.config.html_baseurl
        or not isinstance(app.builder, DirectoryHTMLBuilder)
        or not context["pageurl"]
        or not context["pageurl"].endswith(".html")
    ):
        return

    target = app.builder.get_target_uri(pagename)
    context["pageurl"] = app.config.html_baseurl + target


def adjust_known_instances(icon_link: dict[str, str]) -> dict[str, str]:
    """Adjust icon data for supported self-hostable forge instances."""
    if icon_link["url"].startswith("https://codeberg.org"):
        icon_link["icon"] = (
            r"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 4.233 4.233'%3E%3Cdefs%3E%3ClinearGradient xlink:href='%23a' id='b' x1='42519.285' x2='42575.336' y1='-7078.789' y2='-6966.931' gradientUnits='userSpaceOnUse'/%3E%3ClinearGradient id='a'%3E%3Cstop offset='0' style='stop-color:%232185d0;stop-opacity:0'/%3E%3Cstop offset='.495' style='stop-color:%232185d0;stop-opacity:.30000001'/%3E%3Cstop offset='1' style='stop-color:%232185d0;stop-opacity:.30000001'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M42519.285-7078.79a.76.568 0 0 0-.738.675l33.586 125.888a87.182 87.182 0 0 0 39.381-33.763l-71.565-92.52a.76.568 0 0 0-.664-.28z' style='font-variation-settings:normal;opacity:1;vector-effect:none;fill:url(%23b);fill-opacity:1;stroke:none;stroke-width:3.67846;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:2;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;paint-order:stroke markers fill;stop-color:%23000;stop-opacity:1' transform='translate(-1030.156 172.97) scale(.02428)'/%3E%3Cpath d='M11249.461-1883.696c-12.74 0-23.067 10.327-23.067 23.067 0 4.333 1.22 8.58 3.522 12.251l19.232-24.863c.138-.18.486-.18.624 0l19.233 24.864a23.068 23.068 0 0 0 3.523-12.252c0-12.74-10.327-23.067-23.067-23.067z' style='opacity:1;fill:%232185d0;fill-opacity:1;stroke-width:17.0055;paint-order:markers fill stroke;stop-color:%23000' transform='translate(-1030.156 172.97) scale(.09176)'/%3E%3C/svg%3E"
        )
        icon_link["name"] = "Codeberg"
    return icon_link


def setup(app: Sphinx) -> Dict[str, str]:
    """Setup the Sphinx application."""
    here = Path(__file__).parent.resolve()
    theme_path = here / "theme" / "pydata_sphinx_theme"

    app.add_html_theme("pydata_sphinx_theme", str(theme_path))

    theme_options = utils.get_theme_options_dict(app)
    if theme_options.get("shorten_urls"):
        app.add_post_transform(short_link.ShortenLinkTransform)

    app.connect("builder-inited", translator.setup_translators)
    app.connect("builder-inited", update_config)
    app.connect("html-page-context", _fix_canonical_url)
    app.connect("html-page-context", edit_this_page.setup_edit_url)
    app.connect("html-page-context", toctree.add_toctree_functions)
    app.connect("html-page-context", update_and_remove_templates)
    app.connect("html-page-context", logo.setup_logo_path)
    app.connect("html-page-context", utils.set_secondary_sidebar_items)
    app.connect("build-finished", pygments.overwrite_pygments_css)
    app.connect("build-finished", logo.copy_logo_images)

    # https://www.sphinx-doc.org/en/master/extdev/i18n.html#extension-internationalization-i18n-and-localization-l10n-using-i18n-api
    app.add_message_catalog("sphinx", here / "locale")

    # Include component templates
    app.config.templates_path.append(str(theme_path / "components"))

    return {"parallel_read_safe": True, "parallel_write_safe": True}
