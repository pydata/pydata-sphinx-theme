/* Sphinx injects the html output with jquery and other javascript files.
 * To enable Popper.js (and other jQuery plugins) to hook into the same instance of jQuery,
 * jQuery is defined as a Webpack external, thus this import uses the externally defined jquery dependency.
 */
import "jquery";

import "popper.js";
import "bootstrap";

import "../styles/index.scss";

////////////////////////////////////////////////////////////////////////////////
// TOC interactivity
////////////////////////////////////////////////////////////////////////////////

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
  var sidebar = document.getElementById("bd-docs-nav");

  // Remember the sidebar scroll position between page loads
  // Inspired on source of revealjs.com
  let storedScrollTop = parseInt(
    sessionStorage.getItem("sidebar-scroll-top"),
    10
  );

  if (!isNaN(storedScrollTop)) {
    sidebar.scrollTop = storedScrollTop;
  } else {
    var active_pages = sidebar.querySelectorAll(".active");
    var offset = 0;
    var i;
    for (i = active_pages.length - 1; i > 0; i--) {
      var active_page = active_pages[i];
      if (active_page !== undefined) {
        offset += active_page.offsetTop;
      }
    }
    offset -= sidebar.offsetTop;

    // Only scroll the navbar if the active link is lower than 50% of the page
    if (active_page !== undefined && offset > sidebar.clientHeight * 0.5) {
      sidebar.scrollTop = offset - sidebar.clientHeight * 0.2;
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

function autoTheme(e) {
  document.body.dataset.theme = prefersDark.matches ? "dark" : "light";
}

function setTheme(mode) {
  if (mode !== "light" && mode !== "dark" && mode !== "auto") {
    console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
    mode = "auto";
  }

  // get the theme
  var colorScheme = prefersDark.matches ? "dark" : "light";
  document.body.dataset.theme = mode == "auto" ? colorScheme : mode;

  // save mode
  localStorage.setItem("theme", mode);
  console.log(`Changed to ${mode} mode.`);

  // change btn visibillity
  const btnList = document.getElementsByClassName("theme-switch");
  Array.from(btnList).forEach((btn) => {
    btn.style.display = btn.dataset.mode == mode ? "block" : "none";
  });

  // add a listener if set on auto
  prefersDark.onchange = mode == "auto" ? autoTheme : "";
}

function cycleTheme() {
  const currentTheme = localStorage.getItem("theme") || "auto";

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

function setupTheme() {
  // setup at least one time
  const currentTheme = localStorage.getItem("theme") || "auto";
  setTheme(currentTheme);

  // Attach event handlers for toggling themes
  const btnList = document.getElementsByClassName("theme-switch");
  Array.from(btnList).forEach((btn) => {
    btn.addEventListener("click", cycleTheme);
  });
}

$(document).ready(() => {
  setupTheme();
  scrollToActive();
  addTOCInteractivity();
});
