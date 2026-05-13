import { dom, library } from "@fortawesome/fontawesome-svg-core";

dom.watch();

// Expose globally so user scripts (custom-icons.js) and the
// generated fontawesome-user-icons.js can call library.add / dom.i2svg.
window.FontAwesome = { dom, library };
