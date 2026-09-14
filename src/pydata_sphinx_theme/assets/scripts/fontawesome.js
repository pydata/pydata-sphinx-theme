import {
  config,
  dom,
  library,
  icon,
  parse,
  findIconDefinition,
} from "@fortawesome/fontawesome-svg-core";

// Standard icons come from CSS + webfonts; only custom icons need JS.
config.autoReplaceSvg = false;

// Public API, notably library.add() in users' custom-icons.js.
window.FontAwesome = { config, dom, library, icon, parse, findIconDefinition };

function renderCustomIcons() {
  document
    .querySelectorAll("i.fa-custom")
    .forEach((node) => dom.i2svg({ node: node.parentNode }));
}

// After deferred scripts, so library.add() has run.
if (document.readyState === "complete") {
  renderCustomIcons();
} else {
  document.addEventListener("DOMContentLoaded", renderCustomIcons);
}
