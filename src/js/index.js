/**
 * This file should be edited in ./src/js/index.js. After bundling the resulting file in ./pydata_sphinx_theme/static/js/index.js should never be manually changed.
 * Edit ./src/js/index.js and run yarn build:dev or yarn build:production.
 */

// TOC sidebar - add "active" class to parent list
//
// Bootstrap's scrollspy adds the active class to the <a> link,
// but for the automatic collapsing we need this on the parent list item.
//
// The event is triggered on "window" (and not the nav item as documented),
// see https://github.com/twbs/bootstrap/issues/20086
$(window).on('activate.bs.scrollspy', function() {
  const navLinks = document.querySelectorAll('#bd-toc-nav a');

  navLinks.forEach(navLink => {
    navLink.parentElement.classList.remove('active');
  })

  const activeNavLinks = document.querySelectorAll('#bd-toc-nav a.active');
  activeNavLinks.forEach(navLink => {
    navLink.parentElement.classList.add('active');
  })
});
