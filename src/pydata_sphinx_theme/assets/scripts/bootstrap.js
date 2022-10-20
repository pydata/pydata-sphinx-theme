/* Import and setup functions to control Bootstrap's behavior.
 */
import "@popperjs/core";
import { Tooltip } from "bootstrap";

import "../styles/bootstrap.scss";

/*******************************************************************************
 * Trigger tooltips
 */

var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new Tooltip(tooltipTriggerEl);
});
