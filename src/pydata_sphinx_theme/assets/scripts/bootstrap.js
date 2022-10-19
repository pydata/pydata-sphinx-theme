/* Import and setup functions to control Bootstrap's behavior.
 * To enable Popper.js (and other jQuery plugins) to hook into the same instance of jQuery,
 * jQuery is defined as a Webpack external, thus this import uses the externally defined jquery dependency.
 */
import "jquery";
import "popper.js";
import "bootstrap";

import "../styles/bootstrap.scss";

/*******************************************************************************
 * Call function after docuemnt finish loading
 * This is equivalent to the .ready() function as described in
 * https://api.jquery.com/ready/
 */

$('[data-toggle="tooltip"]').tooltip({ delay: { show: 500, hide: 100 } });
