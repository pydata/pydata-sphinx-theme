/* Sphinx injects the html output with jquery and other javascript files.
 * To enable Popper.js (and other jQuery plugins) to hook into the same instance of jQuery,
 * jQuery is defined as a Webpack external, thus this import uses the externally defined jquery dependency.
 */
import "jquery";

import "popper.js";
import "bootstrap";

import "../styles/index.scss";

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

// Navigation sidebar scrolling to active page
function scrollToActive() {
  var sidebar = document.querySelector("div.bd-sidebar");
  var sidebarNav = document.getElementById("bd-docs-nav");

  // Remember the sidebar scroll position between page loads
  // Inspired on source of revealjs.com
  let storedScrollTop = parseInt(
    sessionStorage.getItem("sidebar-scroll-top"),
    10
  );

  if (!isNaN(storedScrollTop)) {
    // If we've got a saved scroll position, just use that
    sidebar.scrollTop = storedScrollTop;
  } else {
    // Otherwise, calculate a position to scroll to based on the lowest `active` link
    var active_pages = sidebarNav.querySelectorAll(".active");
    if (active_pages.length > 0) {
      // Use the last active page as the offset since it's the page we're on
      var offset = active_pages[active_pages.length - 1].offsetTop;
      // Only scroll the navbar if the active link is lower than 50% of the page
      if (offset > sidebar.clientHeight * 0.5) {
        sidebar.scrollTop = offset - sidebar.clientHeight * 0.2;
      }
    }
  }

  // Store the sidebar scroll position
  window.addEventListener("beforeunload", () => {
    sessionStorage.setItem("sidebar-scroll-top", sidebar.scrollTop);
  });
}

// This is equivalent to the .ready() function as described in
// https://api.jquery.com/ready/
$(scrollToActive());
$(addTOCInteractivity());
