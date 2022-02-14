/* Sphinx injects the html output with jquery and other javascript files.
 * To enable Popper.js (and other jQuery plugins) to hook into the same instance of jQuery,
 * jQuery is defined as a Webpack external, thus this import uses the externally defined jquery dependency.
 */
import "jquery";

import "popper.js";
import "bootstrap";

import "../styles/index.scss";

/**
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

////////////////////////////////////////////////////////////////////////////////
// Scroll
////////////////////////////////////////////////////////////////////////////////

// Navigation sidebar scrolling to active page
function scrollToActive() {
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

////////////////////////////////////////////////////////////////////////////////
// Theme interaction
////////////////////////////////////////////////////////////////////////////////
var prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

/**
 * set the the body theme to the one specified by the user browser
 * @param {event} e 
 */
function autoTheme(e) {
  document.body.dataset.theme = prefersDark.matches ? "dark" : "light";
}


/**
 * Set the theme to the specified mode. 
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
  document.body.dataset.mode = mode;
  document.body.dataset.theme = mode == "auto" ? colorScheme : mode;

  // save mode
  localStorage.setItem("theme", mode);
  console.log(`Changed to ${mode} mode.`);

  // add a listener if set on auto
  prefersDark.onchange = mode == "auto" ? autoTheme : "";
}

/**
 * Change the theme option order so that clicking on the btn is always a change
 * from "auto"
 */
function cycleTheme() {
  const defaultMode = document.body.dataset.defaultMode || "auto";
  const currentTheme = localStorage.getItem("theme") || defaultMode;

  if (prefersDark.matches) {
    // Auto (dark) -> Light -> Dark
    if (currentTheme === "auto") {
      setTheme("light");
    } else if (currentTheme == "light") {
      setTheme("dark");
    } else {
      setTheme("auto");
    }
  } else {
    // Auto (light) -> Dark -> Light
    if (currentTheme === "auto") {
      setTheme("dark");
    } else if (currentTheme == "dark") {
      setTheme("light");
    } else {
      setTheme("auto");
    }
  }
}

/**
 * setup the theme color based on the prefered mode and the browser options
 * should be called when entering the doc to fill localStorage
 */
function setupTheme() {
  // setup at least one time
  const defaultMode = document.body.dataset.defaultMode || "auto";
  const currentTheme = localStorage.getItem("theme") || defaultMode;
  setTheme(currentTheme);

  // Attach event handlers for toggling themes
  const btnList = document.getElementsByClassName("theme-switch");
  Array.from(btnList).forEach((btn) => {
    btn.addEventListener("click", cycleTheme);
  });
}

// This is equivalent to the .ready() function as described in
// https://api.jquery.com/ready/
$(setupTheme);
$(scrollToActive);
$(addTOCInteractivity);
