import {
  config,
  dom,
  library,
  icon,
  parse,
  findIconDefinition,
} from "@fortawesome/fontawesome-svg-core";

// Standard icons render from CSS + webfonts. Disable the page-wide <i>-to-<svg>
// replacement (and its layout flicker); only custom icons, which the webfonts
// can't provide, are converted to inline <svg> below.
config.autoReplaceSvg = false;

// Keep the public API users rely on, notably FontAwesome.library.add() in
// their custom-icons.js.
window.FontAwesome = { config, dom, library, icon, parse, findIconDefinition };

function renderCustomIcons() {
  document
    .querySelectorAll("i.fa-custom")
    .forEach((node) => dom.i2svg({ node: node.parentNode }));
}

// Run after all deferred scripts (including the user's library.add call).
if (document.readyState === "complete") {
  renderCustomIcons();
} else {
  document.addEventListener("DOMContentLoaded", renderCustomIcons);
}
