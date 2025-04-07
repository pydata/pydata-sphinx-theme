// Define the custom behavior of the page
import { documentReady } from "./mixin";
import { compare, validate } from "compare-versions";

import "../styles/pydata-sphinx-theme.scss";

/*******************************************************************************
 * Theme interaction
 */

var prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

/**
 * set the the body theme to the one specified by the user browser
 *
 * @param {event} e
 */
function autoTheme(e) {
  document.documentElement.dataset.theme = prefersDark.matches
    ? "dark"
    : "light";
}

/**
 * Set the theme using the specified mode.
 * It can be one of ["auto", "dark", "light"]
 *
 * @param {str} mode
 */
function setTheme(mode) {
  if (mode !== "light" && mode !== "dark" && mode !== "auto") {
    console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
    mode = "auto";
  }

  // get the theme
  var colorScheme = prefersDark.matches ? "dark" : "light";
  document.documentElement.dataset.mode = mode;
  var theme = mode == "auto" ? colorScheme : mode;
  document.documentElement.dataset.theme = theme;
  // TODO: remove this line after Bootstrap upgrade
  // v5.3 has a colors mode: https://getbootstrap.com/docs/5.3/customize/color-modes/
  document.querySelectorAll(".dropdown-menu").forEach((el) => {
    if (theme === "dark") {
      el.classList.add("dropdown-menu-dark");
    } else {
      el.classList.remove("dropdown-menu-dark");
    }
  });

  // save mode and theme
  localStorage.setItem("mode", mode);
  localStorage.setItem("theme", theme);
  console.log(`[PST]: Changed to ${mode} mode using the ${theme} theme.`);

  // add a listener if set on auto
  prefersDark.onchange = mode == "auto" ? autoTheme : "";
}

/**
 * Change the theme option order so that clicking on the btn is always a change
 * from "auto"
 */
function cycleMode() {
  const defaultMode = document.documentElement.dataset.defaultMode || "auto";
  const currentMode = localStorage.getItem("mode") || defaultMode;

  var loopArray = (arr, current) => {
    var nextPosition = arr.indexOf(current) + 1;
    if (nextPosition === arr.length) {
      nextPosition = 0;
    }
    return arr[nextPosition];
  };

  // make sure the next theme after auto is always a change
  var modeList = prefersDark.matches
    ? ["auto", "light", "dark"]
    : ["auto", "dark", "light"];
  var newMode = loopArray(modeList, currentMode);
  setTheme(newMode);
}

/**
 * add the theme listener on the btns of the navbar
 */
function addModeListener() {
  // the theme was set a first time using the initial mini-script
  // running setMode will ensure the use of the dark mode if auto is selected
  setTheme(document.documentElement.dataset.mode);

  // Attach event handlers for toggling themes colors
  document.querySelectorAll(".theme-switch-button").forEach((el) => {
    el.addEventListener("click", cycleMode);
  });
}

/*******************************************************************************
 * Scroll
 */

/**
 * Navigation sidebar scrolling to active page
 */
function scrollToActive() {
  // If the docs nav doesn't exist, do nothing (e.g., on search page)
  if (!document.querySelector(".bd-docs-nav")) {
    return;
  }

  var sidebar = document.querySelector("div.bd-sidebar");

  // Remember the sidebar scroll position between page loads
  // Inspired on source of revealjs.com
  let storedScrollTop = parseInt(
    sessionStorage.getItem("sidebar-scroll-top"),
    10,
  );

  if (!isNaN(storedScrollTop)) {
    // If we've got a saved scroll position, just use that
    sidebar.scrollTop = storedScrollTop;
    console.log("[PST]: Scrolled sidebar using stored browser position...");
  } else {
    // Otherwise, calculate a position to scroll to based on the lowest `active` link
    var sidebarNav = document.querySelector(".bd-docs-nav");
    var active_pages = sidebarNav.querySelectorAll(".active");
    if (active_pages.length > 0) {
      // Use the last active page as the offset since it's the page we're on
      var latest_active = active_pages[active_pages.length - 1];
      var offset =
        latest_active.getBoundingClientRect().y -
        sidebar.getBoundingClientRect().y;
      // Only scroll the navbar if the active link is lower than 50% of the page
      if (latest_active.getBoundingClientRect().y > window.innerHeight * 0.5) {
        let buffer = 0.25; // Buffer so we have some space above the scrolled item
        sidebar.scrollTop = offset - sidebar.clientHeight * buffer;
        console.log("[PST]: Scrolled sidebar using last active link...");
      }
    }
  }

  // Store the sidebar scroll position
  window.addEventListener("beforeunload", () => {
    sessionStorage.setItem("sidebar-scroll-top", sidebar.scrollTop);
  });
}

/*******************************************************************************
 * Search
 */

/**
 * Find any search forms on the page and return their input element
 */
var findSearchInput = () => {
  let forms = document.querySelectorAll("form.bd-search");
  if (!forms.length) {
    // no search form found
    return;
  } else {
    var form;
    if (forms.length == 1) {
      // there is exactly one search form (persistent or hidden)
      form = forms[0];
    } else {
      // must be at least one persistent form, use the first persistent one
      form = document.querySelector(
        ":not(#pst-search-dialog) > form.bd-search",
      );
    }
    return form.querySelector("input");
  }
};

/**
 * Activate the search field on the page.
 * - If there is a search field already visible it will be activated.
 * - If not, then a search field will pop up.
 */
var toggleSearchField = () => {
  // Find the search input to highlight
  const input = findSearchInput();

  // if the input field is the hidden one (the one associated with the
  // search button) then toggle the button state (to show/hide the field)
  const searchDialog = document.getElementById("pst-search-dialog");
  const hiddenInput = searchDialog.querySelector("input");
  if (input === hiddenInput) {
    if (searchDialog.open) {
      searchDialog.close();
    } else {
      // Note: browsers should focus the input field inside the modal dialog
      // automatically when it is opened.
      searchDialog.showModal();
    }
  } else {
    // if the input field is not the hidden one, then toggle its focus state

    if (document.activeElement === input) {
      input.blur();
    } else {
      input.focus();
      input.select();
      input.scrollIntoView({ block: "center" });
    }
  }
};

/**
 * Add an event listener for toggleSearchField() for Ctrl/Cmd + K
 */
var addEventListenerForSearchKeyboard = () => {
  window.addEventListener(
    "keydown",
    (event) => {
      let input = findSearchInput();
      // toggle on Ctrl+k or ⌘+k
      if (
        // Ignore if shift or alt are pressed
        !event.shiftKey &&
        !event.altKey &&
        // On Mac use ⌘, all other OS use Ctrl
        (useCommandKey
          ? event.metaKey && !event.ctrlKey
          : !event.metaKey && event.ctrlKey) &&
        // Case-insensitive so the shortcut still works with caps lock
        /^k$/i.test(event.key)
      ) {
        event.preventDefault();
        toggleSearchField();
      }
      // also allow Escape key to hide (but not show) the dynamic search field
      else if (document.activeElement === input && /Escape/i.test(event.key)) {
        toggleSearchField();
        resetSearchAsYouTypeResults();
      }
    },
    true,
  );
};

/**
 * If the user is on a Mac, use command (⌘) instead of control (ctrl) key
 *
 * Note: `navigator.platform` is deprecated; however MDN still recommends using
 * it for the one specific use case of detecting whether a keyboard shortcut
 * should use control or command:
 * https://developer.mozilla.org/en-US/docs/Web/API/Navigator/platform#examples
 */
var useCommandKey =
  navigator.platform.indexOf("Mac") === 0 || navigator.platform === "iPhone";

/**
 * Change the search hint to `meta key` if we are a Mac
 */

var changeSearchShortcutKey = () => {
  let shortcuts = document.querySelectorAll(".search-button__kbd-shortcut");
  if (useCommandKey) {
    shortcuts.forEach(
      (f) => (f.querySelector("kbd.kbd-shortcut__modifier").innerText = "⌘"),
    );
  }
};

const closeDialogOnBackdropClick = ({
  currentTarget: dialog,
  clientX,
  clientY,
}) => {
  if (!dialog.open) {
    return;
  }

  // Dialog.getBoundingClientRect() does not include ::backdrop. (This is the
  // trick that allows us to determine if click was inside or outside of the
  // dialog: click handler includes backdrop, getBoundingClientRect does not.)
  const { left, right, top, bottom } = dialog.getBoundingClientRect();

  // 0, 0 means top left
  const clickWasOutsideDialog =
    clientX < left || right < clientX || clientY < top || bottom < clientY;

  if (clickWasOutsideDialog) {
    dialog.close();
  }
};

/**
 * Activate callbacks for search button popup
 */
var setupSearchButtons = () => {
  changeSearchShortcutKey();
  addEventListenerForSearchKeyboard();

  // Add the search button trigger event callback
  document.querySelectorAll(".search-button__button").forEach((btn) => {
    btn.onclick = toggleSearchField;
  });

  // If user clicks outside the search modal dialog, then close it.
  const searchDialog = document.getElementById("pst-search-dialog");
  // Dialog click handler includes clicks on dialog ::backdrop.
  searchDialog.addEventListener("click", closeDialogOnBackdropClick);
};

/*******************************************************************************
 * Inline search results (search-as-you-type)
 *
 * Immediately displays search results under the search query textbox.
 *
 * The search is conducted by Sphinx's built-in search tools (searchtools.js).
 * Usually searchtools.js is only available on /search.html but
 * pydata-sphinx-theme (PST) has been modified to load searchtools.js on every
 * page. After the user types something into PST's search query textbox,
 * searchtools.js executes the search and populates the results into
 * the #search-results container. searchtools.js expects the results container
 * to have that exact ID.
 */
var setupSearchAsYouType = () => {
  if (!DOCUMENTATION_OPTIONS.search_as_you_type) {
    return;
  }

  // Don't interfere with the default search UX on /search.html.
  if (window.location.pathname.endsWith("/search.html")) {
    return;
  }

  // Bail if the Search class is not available. Search-as-you-type is
  // impossible without that class. layout.html should ensure that
  // searchtools.js loads.
  //
  // Search class is defined in upstream Sphinx:
  // https://github.com/sphinx-doc/sphinx/blob/6678e357048ea1767daaad68e7e0569786f3b458/sphinx/themes/basic/static/searchtools.js#L181
  if (!Search) {
    return;
  }

  // Destroy the previous search container and create a new one.
  resetSearchAsYouTypeResults();
  let timeoutId = null;
  let lastQuery = "";
  const searchInput = document.querySelector(
    "#pst-search-dialog input[name=q]",
  );

  // Initiate searches whenever the user types stuff in the search modal textbox.
  searchInput.addEventListener("keyup", () => {
    const query = searchInput.value;

    // Don't search when there's nothing in the query textbox.
    if (query === "") {
      lastQuery = "";
      resetSearchAsYouTypeResults(); // Remove previous results.
      return;
    }

    // Don't search if there is no detectable change between
    // the last query and the current query. E.g. the user presses
    // Tab to start navigating the search results.
    if (query === lastQuery) {
      return;
    }

    // The user has changed the search query. Delete the old results
    // and start setting up the new container.
    resetSearchAsYouTypeResults();

    // Debounce so that the search only starts when the user stops typing.
    const delay_ms = 300;
    lastQuery = query;
    if (timeoutId) {
      window.clearTimeout(timeoutId);
    }
    timeoutId = window.setTimeout(() => {
      Search.performSearch(query);
      document.querySelector("#search-results").classList.remove("empty");
      timeoutId = null;
    }, delay_ms);
  });
};

// Delete the old search results container (if it exists) and set up a new one.
//
// There is some complexity around ensuring that the search results links are
// correct because we're extending searchtools.js past its assumed usage.
// Sphinx assumes that searches are only executed from /search.html and
// therefore it assumes that all search results links should be relative to
// the root directory of the website. In our case the search can now execute
// from any page of the website so we must fix the relative URLs that
// searchtools.js generates.
var resetSearchAsYouTypeResults = () => {
  if (!DOCUMENTATION_OPTIONS.search_as_you_type) {
    return;
  }
  // If a search-as-you-type results container was previously added,
  // remove it now.
  let results = document.querySelector("#search-results");
  if (results) {
    results.remove();
  }

  // Create a new search-as-you-type results container.
  results = document.createElement("section");
  results.classList.add("empty");
  // Remove the container element from the tab order. Individual search
  // results are still focusable.
  results.tabIndex = -1;
  // When focus is on a search result, make sure that pressing Escape closes
  // the search modal.
  results.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      event.stopPropagation();
      toggleSearchField();
      resetSearchAsYouTypeResults();
    }
  });
  // IMPORTANT: The search results container MUST have this exact ID.
  // searchtools.js is hardcoded to populate into the node with this ID.
  results.id = "search-results";
  let modal = document.querySelector("#pst-search-dialog");
  modal.appendChild(results);

  // Get the relative path back to the root of the website.
  const root =
    "URL_ROOT" in DOCUMENTATION_OPTIONS
      ? DOCUMENTATION_OPTIONS.URL_ROOT // Sphinx v6 and earlier
      : document.documentElement.dataset.content_root; // Sphinx v7 and later

  // As Sphinx populates the search results, this observer makes sure that
  // each URL is correct (i.e. doesn't 404).
  const linkObserver = new MutationObserver(() => {
    const links = Array.from(
      document.querySelectorAll("#search-results .search a"),
    );
    // Check every link every time because the timing of when new results are
    // added is unpredictable and it's not an expensive operation.
    links.forEach((link) => {
      link.tabIndex = 0; // Use natural tab order for search results.
      // Don't use the link.href getter because the browser computes the href
      // as a full URL. We need the relative URL that Sphinx generates.
      const href = link.getAttribute("href");
      if (href.startsWith(root)) {
        // No work needed. The root has already been prepended to the href.
        return;
      }
      link.href = `${root}${href}`;
    });
  });

  // The node that linkObserver watches doesn't exist until the user types
  // something into the search textbox. This second observer (resultsObserver)
  // just waits for #search-results to exist and then registers
  // linkObserver on it.
  let isObserved = false;
  const resultsObserver = new MutationObserver(() => {
    if (isObserved) {
      return;
    }
    const container = document.querySelector("#search-results .search");
    if (!container) {
      return;
    }
    linkObserver.observe(container, { childList: true });
    isObserved = true;
  });
  resultsObserver.observe(results, { childList: true });
};

/*******************************************************************************
 * Version Switcher
 * Note that this depends on two variables existing that are defined in
 * and `html-page-context` hook:
 *
 * - DOCUMENTATION_OPTIONS.pagename
 * - DOCUMENTATION_OPTIONS.theme_switcher_url
 */

/**
 * path component of URL
 */
var getCurrentUrlPath = () => {
  if (DOCUMENTATION_OPTIONS.BUILDER == "dirhtml") {
    return DOCUMENTATION_OPTIONS.pagename.endsWith("index")
      ? `${DOCUMENTATION_OPTIONS.pagename.substring(0, DOCUMENTATION_OPTIONS.pagename.length - "index".length)}`
      : `${DOCUMENTATION_OPTIONS.pagename}/`;
  }
  return `${DOCUMENTATION_OPTIONS.pagename}.html`;
};

/**
 * Allow user to dismiss the warning banner about the docs version being dev / old.
 * We store the dismissal date and version, to give us flexibility about making the
 * dismissal last for longer than one browser session, if we decide to do that.
 *
 * @param {event} event the event that trigger the check
 */
async function DismissBannerAndStorePref(event) {
  const banner = document.querySelector("#bd-header-version-warning");
  banner.remove();
  const version = DOCUMENTATION_OPTIONS.VERSION;
  const now = new Date();
  const banner_pref = JSON.parse(
    localStorage.getItem("pst_banner_pref") || "{}",
  );
  console.debug(
    `[PST] Dismissing the version warning banner on ${version} starting ${now}.`,
  );
  banner_pref[version] = now;
  localStorage.setItem("pst_banner_pref", JSON.stringify(banner_pref));
}

/**
 * Check if corresponding page path exists in other version of docs
 * and, if so, go there instead of the homepage of the other docs version
 *
 * @param {event} event the event that trigger the check
 */
async function checkPageExistsAndRedirect(event) {
  // ensure we don't follow the initial link
  event.preventDefault();
  const currentFilePath = getCurrentUrlPath();
  let tryUrl = event.currentTarget.getAttribute("href");
  let otherDocsHomepage = tryUrl.replace(currentFilePath, "");
  try {
    let head = await fetch(tryUrl, { method: "HEAD" });
    if (head.ok) {
      location.href = tryUrl; // the page exists, go there
    } else {
      location.href = otherDocsHomepage;
    }
  } catch (err) {
    // something went wrong, probably CORS restriction, fallback to other docs homepage
    location.href = otherDocsHomepage;
  }
}

/**
 * Load and parse the version switcher JSON file from an absolute or relative URL.
 *
 * @param {string} url The URL to load version switcher entries from.
 */
async function fetchVersionSwitcherJSON(url) {
  const currentPath = getCurrentUrlPath();
  // first check if it's a valid URL
  try {
    var result = new URL(url);
  } catch (err) {
    if (err instanceof TypeError) {
      // Assume we got a relative path, and fix accordingly.
      if (window.location.protocol == "file:") {
        // Here instead of returning `null` we work out what the file path would be
        // anyway (same code path as for served docs), as a convenience to folks who
        // routinely disable CORS when they boot up their browser.
        console.info(
          "[PST] looks like you're viewing this site from a local filesystem, so " +
            "the version switcher won't work unless you've disabled CORS. See " +
            "https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/version-dropdown.html",
        );
      }
      const cutoff = window.location.href.indexOf(currentPath);
      // cutoff == -1 can happen e.g. on the homepage of locally served docs, where you
      // get something like http://127.0.0.1:8000/ (no trailing `index.html`)
      const origin =
        cutoff == -1
          ? window.location.href
          : window.location.href.substring(0, cutoff);
      result = new URL(url, origin);
    } else {
      // something unexpected happened
      throw err;
    }
  }
  // load and return the JSON
  const response = await fetch(result);
  const data = await response.json();
  return data;
}

// Populate the version switcher from the JSON data
function populateVersionSwitcher(data, versionSwitcherBtns) {
  const currentFilePath = getCurrentUrlPath();
  versionSwitcherBtns.forEach((btn) => {
    // Set empty strings by default so that these attributes exist and can be used in CSS selectors
    btn.dataset["activeVersionName"] = "";
    btn.dataset["activeVersion"] = "";
  });
  // in case there are multiple entries with the same version string, this helps us
  // decide which entry's `name` to put on the button itself. Without this, it would
  // always be the *last* version-matching entry; now it will be either the
  // version-matching entry that is also marked as `"preferred": true`, or if that
  // doesn't exist: the *first* version-matching entry.
  data = data.map((entry) => {
    // does this entry match the version that we're currently building/viewing?
    entry.match =
      entry.version == DOCUMENTATION_OPTIONS.theme_switcher_version_match;
    entry.preferred = entry.preferred || false;
    // if no custom name specified (e.g., "latest"), use version string
    if (!("name" in entry)) {
      entry.name = entry.version;
    }
    return entry;
  });
  const hasMatchingPreferredEntry = data
    .map((entry) => entry.preferred && entry.match)
    .some(Boolean);
  var foundMatch = false;
  // create links to the corresponding page in the other docs versions
  data.forEach((entry) => {
    // create the node
    const anchor = document.createElement("a");
    anchor.setAttribute(
      "class",
      "dropdown-item list-group-item list-group-item-action py-1",
    );
    anchor.setAttribute("href", `${entry.url}${currentFilePath}`);
    anchor.setAttribute("role", "option");
    const span = document.createElement("span");
    span.textContent = `${entry.name}`;
    anchor.appendChild(span);
    // Add dataset values for the version and name in case people want
    // to apply CSS styling based on this information.
    anchor.dataset["versionName"] = entry.name;
    anchor.dataset["version"] = entry.version;
    // replace dropdown button text with the preferred display name of the
    // currently-viewed version, rather than using sphinx's {{ version }} variable.
    // also highlight the dropdown entry for the currently-viewed version's entry
    let matchesAndIsPreferred = hasMatchingPreferredEntry && entry.preferred;
    let matchesAndIsFirst =
      !hasMatchingPreferredEntry && !foundMatch && entry.match;
    if (matchesAndIsPreferred || matchesAndIsFirst) {
      anchor.classList.add("active");
      versionSwitcherBtns.forEach((btn) => {
        btn.innerText = entry.name;
        btn.dataset["activeVersionName"] = entry.name;
        btn.dataset["activeVersion"] = entry.version;
      });
      foundMatch = true;
    }
    // There may be multiple version-switcher elements, e.g. one
    // in a slide-over panel displayed on smaller screens.
    document.querySelectorAll(".version-switcher__menu").forEach((menu) => {
      // we need to clone the node for each menu, but onclick attributes are not
      // preserved by `.cloneNode()` so we add onclick here after cloning.
      let node = anchor.cloneNode(true);
      node.onclick = checkPageExistsAndRedirect;
      // on click, AJAX calls will check if the linked page exists before
      // trying to redirect, and if not, will redirect to the homepage
      // for that version of the docs.
      menu.append(node);
    });
  });
}

/*******************************************************************************
 * Warning banner when viewing non-stable version of the docs.
 */

/**
 * Show a warning banner when viewing a non-stable version of the docs.
 *
 * adapted 2023-06 from https://mne.tools/versionwarning.js, which was
 * originally adapted 2020-05 from https://scikit-learn.org/versionwarning.js
 *
 * @param {Array} data The version data used to populate the switcher menu.
 */
function showVersionWarningBanner(data) {
  var version = DOCUMENTATION_OPTIONS.VERSION;
  // figure out what latest stable version is
  var preferredEntries = data.filter((entry) => entry.preferred);
  if (preferredEntries.length !== 1) {
    const howMany = preferredEntries.length == 0 ? "No" : "Multiple";
    console.log(
      `[PST] ${howMany} versions marked "preferred" found in versions JSON, ignoring.`,
    );
    return;
  }
  const preferredVersion = preferredEntries[0].version;
  const preferredURL = preferredEntries[0].url;
  // if already on preferred version, nothing to do
  const versionsAreComparable = validate(version) && validate(preferredVersion);
  if (versionsAreComparable && compare(version, preferredVersion, "=")) {
    console.log(
      "[PST]: This is the preferred version of the docs, not showing the warning banner.",
    );
    return;
  }
  // check if banner has been dismissed recently
  const dismiss_date_str = JSON.parse(
    localStorage.getItem("pst_banner_pref") || "{}",
  )[version];
  if (dismiss_date_str != null) {
    const dismiss_date = new Date(dismiss_date_str);
    const now = new Date();
    const milliseconds_in_a_day = 24 * 60 * 60 * 1000;
    const days_passed = (now - dismiss_date) / milliseconds_in_a_day;
    const timeout_in_days = 14;
    if (days_passed < timeout_in_days) {
      console.info(
        `[PST] Suppressing version warning banner; was dismissed ${Math.floor(
          days_passed,
        )} day(s) ago`,
      );
      return;
    }
  }

  // now construct the warning banner
  const banner = document.querySelector("#bd-header-version-warning");
  const middle = document.createElement("div");
  const inner = document.createElement("div");
  const bold = document.createElement("strong");
  const button = document.createElement("a");
  const close_btn = document.createElement("a");
  // these classes exist since pydata-sphinx-theme v0.10.0
  // the init class is used for animation
  middle.classList = "bd-header-announcement__content  ms-auto me-auto";
  inner.classList = "sidebar-message";
  button.classList =
    "btn text-wrap font-weight-bold ms-3 my-1 align-baseline pst-button-link-to-stable-version";
  button.href = `${preferredURL}${getCurrentUrlPath()}`;
  button.innerText = "Switch to stable version";
  button.onclick = checkPageExistsAndRedirect;
  close_btn.classList = "ms-3 my-1 align-baseline";
  const close_x = document.createElement("i");
  close_btn.append(close_x);
  close_x.classList = "fa-solid fa-xmark";
  close_btn.onclick = DismissBannerAndStorePref;
  // add the version-dependent text
  inner.innerText = "This is documentation for ";
  const isDev =
    version.includes("dev") ||
    version.includes("rc") ||
    version.includes("pre");
  const newerThanPreferred =
    versionsAreComparable && compare(version, preferredVersion, ">");
  if (isDev || newerThanPreferred) {
    bold.innerText = "an unstable development version";
  } else if (versionsAreComparable && compare(version, preferredVersion, "<")) {
    bold.innerText = `an old version (${version})`;
  } else if (!version) {
    bold.innerText = "an unknown version"; // e.g., an empty string
  } else {
    bold.innerText = `version ${version}`;
  }
  banner.appendChild(middle);
  banner.append(close_btn);
  middle.appendChild(inner);
  inner.appendChild(bold);
  inner.appendChild(document.createTextNode("."));
  inner.appendChild(button);
  banner.classList.remove("d-none");
}

async function fetchAndUseVersions() {
  // fetch the JSON version data (only once), then use it to populate the version
  // switcher and maybe show the version warning bar
  var versionSwitcherBtns = document.querySelectorAll(
    ".version-switcher__button",
  );
  const hasSwitcherMenu = versionSwitcherBtns.length > 0;
  const hasVersionsJSON = DOCUMENTATION_OPTIONS.hasOwnProperty(
    "theme_switcher_json_url",
  );
  const wantsWarningBanner = DOCUMENTATION_OPTIONS.show_version_warning_banner;

  if (hasVersionsJSON && (hasSwitcherMenu || wantsWarningBanner)) {
    const data = await fetchVersionSwitcherJSON(
      DOCUMENTATION_OPTIONS.theme_switcher_json_url,
    );
    // TODO: remove the `if(data)` once the `return null` is fixed within fetchVersionSwitcherJSON.
    // We don't really want the switcher and warning bar to silently not work.
    if (data) {
      populateVersionSwitcher(data, versionSwitcherBtns);
      if (wantsWarningBanner) {
        showVersionWarningBanner(data);
      }
    }
  }
}

/*******************************************************************************
 * Sidebar modals (for mobile / narrow screens)
 */
function setupMobileSidebarKeyboardHandlers() {
  // These are the left and right sidebars for wider screens. We cut and paste
  // the content from these widescreen sidebars into the mobile dialogs, when
  // the user clicks the hamburger icon button
  const primarySidebar = document.getElementById("pst-primary-sidebar");
  const secondarySidebar = document.getElementById("pst-secondary-sidebar");

  // These are the corresponding left/right <dialog> elements, which are empty
  // until the user clicks the hamburger icon
  const primaryDialog = document.getElementById("pst-primary-sidebar-modal");
  const secondaryDialog = document.getElementById(
    "pst-secondary-sidebar-modal",
  );

  // These are the hamburger-style buttons in the header nav bar. They only
  // appear at narrow screen width.
  const primaryToggle = document.querySelector(".primary-toggle");
  const secondaryToggle = document.querySelector(".secondary-toggle");

  // Cut nodes and classes from `from`, paste into/onto `to`
  const cutAndPasteNodesAndClasses = (from, to) => {
    Array.from(from.childNodes).forEach((node) => to.appendChild(node));
    Array.from(from.classList).forEach((cls) => {
      from.classList.remove(cls);
      to.classList.add(cls);
    });
  };

  // Hook up the ways to open and close the dialog
  [
    [primaryToggle, primaryDialog, primarySidebar],
    [secondaryToggle, secondaryDialog, secondarySidebar],
  ].forEach(([toggleButton, dialog, sidebar]) => {
    if (!toggleButton || !dialog || !sidebar) {
      return;
    }

    // Clicking the button can only open the sidebar, not close it.
    // Clicking the button is also the *only* way to open the sidebar.
    toggleButton.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();

      // When we open the dialog, we cut and paste the nodes and classes from
      // the widescreen sidebar into the dialog
      cutAndPasteNodesAndClasses(sidebar, dialog);

      dialog.showModal();
    });

    // Listen for clicks on the backdrop in order to close the dialog
    dialog.addEventListener("click", closeDialogOnBackdropClick);

    // We have to manually attach the escape key because there's some code in
    // Sphinx's Sphinx_highlight.js that prevents the default behavior of the
    // escape key
    dialog.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        event.stopPropagation();
        dialog.close();
      }
    });

    // When the dialog is closed, move the nodes (and classes) back to their
    // original place
    dialog.addEventListener("close", () => {
      cutAndPasteNodesAndClasses(dialog, sidebar);
    });
  });
}

/**
 * When the page loads, or the window resizes, or descendant nodes are added or
 * removed from the main element, check all code blocks and Jupyter notebook
 * outputs, and for each one that has scrollable overflow, set tabIndex = 0.
 */
function addTabStopsToScrollableElements() {
  const updateTabStops = () => {
    document
      .querySelectorAll(
        [
          // code blocks
          "pre",
          // NBSphinx notebook output
          ".nboutput > .output_area",
          // Myst-NB
          ".cell_output > .output",
          // ipywidgets
          ".jp-RenderedHTMLCommon",
          // [rST table nodes](https://www.docutils.org/docs/ref/doctree.html#table)
          ".pst-scrollable-table-container",
        ].join(", "),
      )
      .forEach((el) => {
        el.tabIndex =
          el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight
            ? 0
            : -1;
      });
  };
  const debouncedUpdateTabStops = debounce(updateTabStops, 300);

  // On window resize
  window.addEventListener("resize", debouncedUpdateTabStops);

  // The following MutationObserver is for ipywidgets, which take some time to
  // finish loading and rendering on the page (so even after the "load" event is
  // fired, they still have not finished rendering). Would be nice to replace
  // the MutationObserver if there is a way to hook into the ipywidgets code to
  // know when it is done.
  const mainObserver = new MutationObserver(debouncedUpdateTabStops);

  // On descendant nodes added/removed from main element
  mainObserver.observe(document.getElementById("main-content"), {
    subtree: true,
    childList: true,
  });

  // On page load (when this function gets called)
  updateTabStops();
}
function debounce(callback, wait) {
  let timeoutId = null;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      callback(...args);
    }, wait);
  };
}

/*******************************************************************************
 * Announcement banner - fetch and load remote HTML
 */
async function setupAnnouncementBanner() {
  const banner = document.querySelector(".bd-header-announcement");
  const { pstAnnouncementUrl } = banner ? banner.dataset : null;

  if (!pstAnnouncementUrl) {
    return;
  }

  try {
    const response = await fetch(pstAnnouncementUrl);
    if (!response.ok) {
      throw new Error(
        `[PST]: HTTP response status not ok: ${response.status} ${response.statusText}`,
      );
    }
    let data = await response.text();
    data = data.trim();
    if (data.length === 0) {
      console.log(`[PST]: Empty announcement at: ${pstAnnouncementUrl}`);
      return;
    }
    banner.innerHTML = `<div class="bd-header-announcement__content">${data}</div>`;
    banner.classList.remove("d-none");
  } catch (_error) {
    console.log(`[PST]: Failed to load announcement at: ${pstAnnouncementUrl}`);
    console.error(_error);
  }
}

/*******************************************************************************
 * Reveal (and animate) the banners (version warning, announcement) together
 */
async function fetchRevealBannersTogether() {
  // Wait until finished fetching and loading banners
  await Promise.allSettled([fetchAndUseVersions(), setupAnnouncementBanner()]);

  // The revealer element should have CSS rules that set height to 0, overflow
  // to hidden, and an animation transition on the height (unless the user has
  // turned off animations)
  const revealer = document.querySelector(".pst-async-banner-revealer");
  if (!revealer) {
    return;
  }

  // Remove the d-none (display-none) class to calculate the children heights.
  revealer.classList.remove("d-none");

  // Add together the heights of the element's children
  const height = Array.from(revealer.children).reduce(
    (height, el) => height + el.offsetHeight,
    0,
  );

  // Use the calculated height to give the revealer a non-zero height (if
  // animations allowed, the height change will animate)
  revealer.style.setProperty("height", `${height}px`);

  // Wait for a bit more than 300ms (the transition duration), then set height
  // to auto so the banner can resize if the window is resized.
  setTimeout(() => {
    revealer.style.setProperty("height", "auto");
  }, 320);
}

/**
 * Add the machinery needed to highlight elements in the TOC when scrolling.
 *
 */
function setupArticleTocSyncing() {
  // Right sidebar table of contents container
  const pageToc = document.querySelector("#pst-page-toc-nav");

  // Not all pages have or include a table of contents. (For example, in the PST
  // docs, at the time of this writing: /user_guide/index.html.)
  if (!pageToc) {
    return;
  }

  // The table of contents is a list of .toc-entry items each of which contains
  // a link and possibly a nested list representing one level deeper in the
  // table of contents.
  const tocEntries = Array.from(pageToc.querySelectorAll(".toc-entry"));
  const tocLinks = Array.from(pageToc.querySelectorAll("a"));

  // If there are no links in the TOC, there's no syncing to be done.
  // (Currently, the template does not render the TOC container if there are no
  // TOC links, so this condition should never evaluate to true if the TOC
  // container is found on the page, but should the template change in the
  // future, this check will prevent a runtime error.)
  if (tocLinks.length === 0) {
    return;
  }

  // Create a boolean variable that allows us to turn off the intersection
  // observer (and then later back on). When the website visitor clicks an
  // in-page link, we want that entry in the TOC to be highlighted/activated,
  // NOT whichever TOC link the intersection observer callback would otherwise
  // highlight.
  let disableObserver = false;

  /**
   * Check the hash portion of the page URL. If it matches an entry in the page
   * table of contents, highlight that entry and temporarily disable the
   * intersection observer while the page scrolls to the corresponding heading.
   */
  function syncTocHash() {
    const { hash: pageHash } = window.location;
    if (pageHash.length > 1) {
      const matchingTocLink = tocLinks.find((link) => link.hash === pageHash);
      if (matchingTocLink) {
        disableObserver = true;
        setTimeout(() => {
          // Give the page ample time to finish scrolling, then re-enable the
          // intersection observer.
          disableObserver = false;
        }, 1000);
        activate(matchingTocLink);
      }
    }
  }

  // When the page loads and when the user clicks an in-page link,
  // sync the page's table of contents.
  syncTocHash();
  // Note we cannot use the "hashchange" event because if the user clicks a hash
  // link, scrolls away, then clicks the same hash link again, it will not fire
  // the change event (because it's the same hash), but we still want to re-sync
  // the table of contents.
  window.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      // Defer the sync operation because window.location.hash does not change
      // until after the default action (i.e., the link click) for the event has
      // happened.
      setTimeout(() => {
        syncTocHash();
      }, 0);
    }
  });

  /**
   * Activate an element and its chain of ancestor TOC entries; deactivate
   * everything else in the TOC. Together with the theme CSS, this unfolds
   * the TOC out to the given entry and highlights that entry.
   *
   * @param {HTMLElement} tocLink The TOC entry to be highlighted
   */
  function activate(tocLink) {
    tocLinks.forEach((el) => {
      if (el === tocLink) {
        el.classList.add("active");
        el.setAttribute("aria-current", "true");
      } else {
        el.classList.remove("active");
        el.removeAttribute("aria-current");
      }
    });
    tocEntries.forEach((el) => {
      if (el.contains(tocLink)) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    });
  }

  /**
   * Get the heading in the article associated with the link in the table of contents
   *
   * @param {HTMLElement} tocLink TOC DOM element to use to grab an article heading
   *
   * @returns The article heading that the TOC element links to
   */
  function getHeading(tocLink) {
    const href = tocLink.getAttribute("href");
    if (!href.startsWith("#")) {
      return;
    }
    const id = href.substring(1);
    // There are cases where href="#" (for example, the first one at /examples/kitchen-sink/structure.html)
    if (!id) {
      return;
    }
    // Use getElementById() because querySelector() requires escaping the id string
    const target = document.getElementById(id);
    // Often the target is a section but we want to track section's heading
    const heading = target.querySelector(":is(h1,h2,h3,h4,h5,h6)");
    // Fallback to the target if there is no heading (for example, links on the
    // PST docs page /examples/kitchen-sink/api.html target <dt> elements)
    return heading || target;
  }

  // Map heading elements to their associated TOC links
  const headingsToTocLinks = new Map();
  tocLinks.forEach((tocLink) => {
    const heading = getHeading(tocLink);
    if (heading) {
      headingsToTocLinks.set(heading, tocLink);
    }
  });

  let observer;

  function connectIntersectionObserver() {
    if (observer) {
      observer.disconnect();
    }

    const header = document.querySelector("#pst-header");
    const headerHeight = header.getBoundingClientRect().height;

    // Intersection observer options
    const options = {
      root: null,
      rootMargin: `-${headerHeight}px 0px -70% 0px`, // Use -70% for the bottom margin so that intersection events happen in only the top third of the viewport
      threshold: 0, // Trigger as soon as the heading goes into (or out of) the top 30% of the viewport
    };

    /**
     *
     * @param {IntersectionObserverEntry[]} entries Objects containing threshold-crossing
     * event information
     *
     */
    function callback(entries) {
      if (disableObserver) {
        return;
      }
      const entry = entries.filter((entry) => entry.isIntersecting).pop();
      if (!entry) {
        return;
      }
      const heading = entry.target;
      const tocLink = headingsToTocLinks.get(heading);
      activate(tocLink);
    }

    observer = new IntersectionObserver(callback, options);
    Array.from(headingsToTocLinks.keys()).forEach((heading) => {
      observer.observe(heading);
    });
  }

  // If the user resizes the window, the header height may change and the
  // intersection observer's root margin will need to be recalculated
  window.addEventListener("resize", debounce(connectIntersectionObserver, 300));
  connectIntersectionObserver();
}

/*******************************************************************************
 * Set up expand/collapse button for primary sidebar
 */
function setupCollapseSidebarButton() {
  const button = document.getElementById("pst-collapse-sidebar-button");
  const sidebar = document.getElementById("pst-primary-sidebar");

  // If this page rendered without the button or sidebar, then there's nothing to do.
  if (!button || !sidebar) {
    return;
  }

  const sidebarSections = Array.from(sidebar.children);

  const expandTooltip = new bootstrap.Tooltip(button, {
    title: button.querySelector(".pst-expand-sidebar-label").textContent,

    // In manual testing, relying on Bootstrap to handle "hover" and "focus" was buggy.
    trigger: "manual",

    placement: "left",
    fallbackPlacements: ["right"],

    // Offsetting the tooltip a bit more than the default [0, 0] solves an issue
    // where the appearance of the tooltip triggers a mouseleave event which in
    // turn triggers the call to hide the tooltip. So in certain areas around
    // the button, it would appear to the user that tooltip flashes in and then
    // back out.
    offset: [0, 12],
  });

  const showTooltip = () => {
    // Only show the "expand sidebar" tooltip when the sidebar is not expanded
    if (button.getAttribute("aria-expanded") === "false") {
      expandTooltip.show();
    }
  };
  const hideTooltip = () => {
    expandTooltip.hide();
  };

  function squeezeSidebar(prefersReducedMotion, done) {
    // Before squeezing the sidebar, freeze the widths of its subsections.
    // Otherwise, the subsections will also narrow and cause the text in the
    // sidebar to reflow and wrap, which we don't want. This is necessary
    // because we do not remove the sidebar contents from the layout (with
    // `display: none`). Rather, we hide the contents from both sighted users
    // and screen readers (with `visibility: hidden`). This provides better
    // stability to the overall layout.
    sidebarSections.forEach(
      (el) => (el.style.width = el.getBoundingClientRect().width + "px"),
    );

    const afterSqueeze = () => {
      // After squeezing the sidebar, set aria-expanded to false
      button.setAttribute("aria-expanded", "false"); // "false" is in quotes because HTML attributes are strings

      button.dataset.busy = false;
    };

    if (prefersReducedMotion) {
      sidebar.classList.add("pst-squeeze");
      afterSqueeze();
    } else {
      sidebar.addEventListener("transitionend", function onTransitionEnd() {
        afterSqueeze();
        sidebar.removeEventListener("transitionend", onTransitionEnd);
      });
      sidebar.classList.add("pst-squeeze");
    }
  }

  function expandSidebar(prefersReducedMotion, done) {
    hideTooltip();

    const afterExpand = () => {
      // After expanding the sidebar (which may be delayed by a CSS transition),
      // unfreeze the widths of the subsections that were frozen when the sidebar
      // was squeezed.
      sidebarSections.forEach((el) => (el.style.width = null));

      // After expanding the sidebar, set aria-expanded to "true" - in quotes
      // because HTML attributes are strings.
      button.setAttribute("aria-expanded", "true");

      button.dataset.busy = false;
    };

    if (prefersReducedMotion) {
      sidebar.classList.remove("pst-squeeze");
      afterExpand();
    } else {
      sidebar.addEventListener("transitionend", function onTransitionEnd() {
        afterExpand();
        sidebar.removeEventListener("transitionend", onTransitionEnd);
      });
      sidebar.classList.remove("pst-squeeze");
    }
  }

  button.addEventListener("click", () => {
    if (button.dataset.busy === "true") {
      return;
    }
    button.dataset.busy = "true";

    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion)", // must be in parentheses
    ).matches;

    if (button.getAttribute("aria-expanded") === "true") {
      squeezeSidebar(prefersReducedMotion);
    } else {
      expandSidebar(prefersReducedMotion);
    }
  });

  button.addEventListener("focus", showTooltip);
  button.addEventListener("mouseenter", showTooltip);
  button.addEventListener("mouseleave", hideTooltip);
  button.addEventListener("blur", hideTooltip);
}

/*******************************************************************************
 * Call functions after document loading.
 */

// This one first to kick off the network request for the version warning
// and announcement banner data as early as possible.
documentReady(fetchRevealBannersTogether);

documentReady(addModeListener);
documentReady(scrollToActive);
documentReady(setupSearchButtons);
documentReady(setupSearchAsYouType);
documentReady(setupMobileSidebarKeyboardHandlers);
documentReady(setupArticleTocSyncing);
documentReady(() => {
  try {
    setupCollapseSidebarButton();
  } catch (err) {
    // This exact error message is used in pytest tests
    console.log("[PST] Error setting up collapse sidebar button");
    console.error(err);
  }
});

// Determining whether an element has scrollable content depends on stylesheets,
// so we're checking for the "load" event rather than "DOMContentLoaded"
if (document.readyState === "complete") {
  addTabStopsToScrollableElements();
} else {
  window.addEventListener("load", addTabStopsToScrollableElements);
}
