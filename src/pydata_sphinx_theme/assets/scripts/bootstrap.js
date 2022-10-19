/* Import and setup functions to control Bootstrap's behavior.
 * Sphinx injects the html output with jquery and other javascript files. To enable
 * Popper.js (and other jQuery plugins) to hook into the same instance of jQuery,
 * jQuery is defined as a Webpack external, thus this import uses the externally defined jquery dependency.
 */
import "jquery";
import "popper.js";
import "bootstrap";

import "../styles/bootstrap.scss";

/*******************************************************************************
 * Call functions after document loading.
 * This is equivalent to the .ready() function as described in
 * https://api.jquery.com/ready/
 */

$('[data-toggle="tooltip"]').tooltip({ delay: { show: 500, hide: 100 } });
