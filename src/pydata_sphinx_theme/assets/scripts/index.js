/* Sphinx injects the html output with jquery and other javascript files.
 * To enable Popper.js (and other jQuery plugins) to hook into the same instance of jQuery,
 * jQuery is defined as a Webpack external, thus this import uses the externally defined jquery dependency.
 */
import "jquery";

import "popper.js";
import "bootstrap";

import "../styles/index.scss";

/*******************************************************************************
 * Theme interaction
 */

var prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

/**
 * set the the body theme to the one specified by the user browser
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
  const btn = document.getElementById("theme-switch");
  if (btn != null) {
    btn.addEventListener("click", cycleMode);
  }
}

/*******************************************************************************
 * TOC interactivity
 */

function addTOCInteractivity() {
  // TOC sidebar - add "active" class to parent list
  //
  // Bootstrap's scrollspy adds the active class to the <a> link,
  // but for the automatic collapsing we need this on the parent list item.
  //
  // The event is triggered on "window" (and not the nav item as documented),
  // see https://github.com/twbs/bootstrap/issues/20086
  $(window).on("activate.bs.scrollspy", function () {
    const navLinks = document.querySelectorAll("#bd-toc-nav a");

    navLinks.forEach((navLink) => {
      navLink.parentElement.classList.remove("active");
    });

    const activeNavLinks = document.querySelectorAll("#bd-toc-nav a.active");
    activeNavLinks.forEach((navLink) => {
      navLink.parentElement.classList.add("active");
    });
  });
}

/*******************************************************************************
 * Scroll
 */

// Navigation sidebar scrolling to active page
function scrollToActive() {
  // If the docs nav doesn't exist, do nothing (e.g., on search page)
  if (!document.getElementById("bd-docs-nav")) {
    return;
  }

  var sidebar = document.querySelector("div.bd-sidebar");

  // Remember the sidebar scroll position between page loads
  // Inspired on source of revealjs.com
  let storedScrollTop = parseInt(
    sessionStorage.getItem("sidebar-scroll-top"),
    10
  );

  if (!isNaN(storedScrollTop)) {
    // If we've got a saved scroll position, just use that
    sidebar.scrollTop = storedScrollTop;
    console.log("[PST]: Scrolled sidebar using stored browser position...");
  } else {
    // Otherwise, calculate a position to scroll to based on the lowest `active` link
    var sidebarNav = document.getElementById("bd-docs-nav");
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
var toggleSearchField = () => {
  // Class to make the search field appear and expand the clickable div behind it
  // Note that `.show` will only have an effect on pages that aren't `search.html`
  let button = document.getElementById("bd-search-button");
  button.classList.toggle("show");

  // We'll grab the elements we need to modify for the search field
  let form = document.querySelector("form.bd-search");
  let input = form.querySelector("input");

  // Change the symbol to `meta key` if we are a Mac
  var isMac = window.navigator.platform.toUpperCase().indexOf("MAC") >= 0;
  if (isMac) {
    let kbd = form.querySelector("kbd.kbd-shortcut__modifier");
    kbd.innerText = "⌘";
  }

  // Select the search input field, and focus the page on it
  input.focus();
  input.select();
  input.scrollIntoView({ block: "center" });
};

// Add an event listener for toggleSearchField() for Ctrl/Cmd + K
window.addEventListener(
  "keydown",
  (event) => {
    let button = document.getElementById("bd-search-button");
    let input = document.querySelector("form.bd-search").querySelector("input");
    if ((event.ctrlKey || event.metaKey) && event.code == "KeyK") {
      event.preventDefault();
      toggleSearchField();
    }
    // also allow Escape key to hide (but not show) the dynamic search field
    else if (document.activeElement === input && event.code == "Escape") {
      toggleSearchField();
    }
    // when hiding the search field, remove its focus
    if (!button.classList.contains("show")) {
      input.blur();
    }
  },
  true
);

window.onload = function () {
  let button = document.getElementById("bd-search-button");
  let overlay = document.querySelector("div.search-button__overlay");
  button.onclick = toggleSearchField;
  overlay.onclick = toggleSearchField;
};

/*******************************************************************************
 * Finalize
 */

// This is equivalent to the .ready() function as described in
// https://api.jquery.com/ready/
$(addModeListener);
$(scrollToActive);
$(addTOCInteractivity);
