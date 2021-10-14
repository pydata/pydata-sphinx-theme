
/**
 * This file should be edited in ./src/js/index.js. After bundling the resulting file in ./pydata_sphinx_theme/static/js/index.js should never be manually changed.
 * Edit ./src/js/index.js and run yarn build:dev or yarn build:production.
 */

/* Sphinx injects the html output with jquery and other javascript files.
 * To enable Popper.js (and other jQuery plugins) to hook into the same instancce of jQuery,
 * jQuery is defined as a Webpack external, thus this import uses the externally defined jquery dependency.
 */
import 'jquery';

import 'popper.js';
import 'bootstrap';

import './../scss/index.scss';

function addTOCInteractivity() {
  // TOC sidebar - add "active" class to parent list
  //
  // Bootstrap's scrollspy adds the active class to the <a> link,
  // but for the automatic collapsing we need this on the parent list item.
  //
  // The event is triggered on "window" (and not the nav item as documented),
  // see https://github.com/twbs/bootstrap/issues/20086
  $(window).on('activate.bs.scrollspy', function () {
    const navLinks = document.querySelectorAll('#bd-toc-nav a');

    navLinks.forEach((navLink) => {
      navLink.parentElement.classList.remove('active');
    });

    const activeNavLinks = document.querySelectorAll('#bd-toc-nav a.active');
    activeNavLinks.forEach((navLink) => {
      navLink.parentElement.classList.add('active');
    });
  });
}


// Navigation sidebar scrolling to active page
function scrollToActive() {
  var sidebar = document.getElementById('bd-docs-nav')

  // Remember the sidebar scroll position between page loads
  // Inspired on source of revealjs.com
  let storedScrollTop = parseInt(sessionStorage.getItem('sidebar-scroll-top'), 10);

  if (!isNaN(storedScrollTop)) {
    sidebar.scrollTop = storedScrollTop;
  }
  else {
    var active_pages = sidebar.querySelectorAll(".active")
    var offset = 0
    var i;
    for (i = active_pages.length - 1; i > 0; i--) {
      var active_page = active_pages[i]
      if (active_page !== undefined) {
        offset += active_page.offsetTop
      }
    }
    offset -= sidebar.offsetTop

    // Only scroll the navbar if the active link is lower than 50% of the page
    if (active_page !== undefined && offset > (sidebar.clientHeight * .5)) {
      sidebar.scrollTop = offset - (sidebar.clientHeight * .2)
    }
  }

  // Store the sidebar scroll position
  window.addEventListener('beforeunload', () => {
    sessionStorage.setItem('sidebar-scroll-top', sidebar.scrollTop);
  });
}

function themeSwitch() {
  
  var switch_btn = document.getElementById('theme-switch')
  
  // extract the base name of the files
  var colors_css = document.getElementById('colors-css')
  var pygment_css = document.getElementById('pygment-css')
  var css_basename = colors_css.href.split('/').slice(0,-1).join('/')
  
  switch_btn.addEventListener("click", function (e) {
    
    // get the current status 
    var i_tag = switch_btn.getElementsByTagName('i')[0];
    var light = i_tag.classList.contains('fa-sun');
    
    // toggle the theme
    var new_theme = light ? 'dark' : 'light';
  
    i_tag.classList.toggle('fa-sun')
    i_tag.classList.toggle('fa-moon')
    pygment_css.href = `${css_basename}/${new_theme}-pygment.css`
    colors_css.href = `${css_basename}/${new_theme}-theme.css`
    
  });
  
};


$(document).ready(() => {
  themeSwitch();
  scrollToActive();
  addTOCInteractivity();
});
