// TODO: @trallard might end up moving this to the main JS file
// Import and setup functions to control Bootstrap's behavior.
import "@popperjs/core";
// Import all of Bootstrap's JS
import * as bootstrap from "bootstrap";
import { documentReady } from "./mixin";

/*******************************************************************************
 * Trigger tooltips
 */

/**
 * Add tooltip to each element with the "tooltip" data-bs-toogle class
 */
function TriggerTooltip() {
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]'),
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl, {
      delay: { show: 500, hide: 100 },
    });
  });
}

/**
 * disable theme switch tooltip while the theme switch dropdown is open
 */
function setupThemeSwitchDropdownTooltip() {
  const themeSwitchContainer = document.querySelector(
    ".theme-switch-container",
  );
  if (!themeSwitchContainer) return;

  const themeSwitchTooltip =
    bootstrap.Tooltip.getInstance(themeSwitchContainer);
  if (!themeSwitchTooltip) return;

  themeSwitchContainer.addEventListener("show.bs.dropdown", () => {
    themeSwitchTooltip.hide();
    themeSwitchTooltip.disable();
  });

  themeSwitchContainer.addEventListener("hide.bs.dropdown", () => {
    themeSwitchTooltip.enable();
  });
}

/*******************************************************************************
 * back to top button
 */
function backToTop() {
  var btn = document.getElementById("pst-back-to-top");
  // Config allows button to be disabled, so check it exists
  if (btn) {
    btn.addEventListener("click", function () {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    });
  }
}

function showBackToTop() {
  var btn = document.getElementById("pst-back-to-top");
  var header = document
    .getElementsByClassName("bd-header")[0]
    .getBoundingClientRect();
  window.addEventListener("scroll", function () {
    if (this.oldScroll > this.scrollY && this.scrollY > header.bottom) {
      btn.style.display = "block";
    } else {
      btn.style.display = "none";
    }
    this.oldScroll = this.scrollY;
  });
}

/*******************************************************************************
 * Call functions after document loading.
 */

documentReady(TriggerTooltip);
documentReady(setupThemeSwitchDropdownTooltip);
documentReady(backToTop);
documentReady(showBackToTop);

window.bootstrap = bootstrap;
