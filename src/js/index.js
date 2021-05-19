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

$(document).ready(() => {
  scrollToActive();
  addTOCInteractivity();
});

function setupVersionSwitcher() {
  // Setup Version Switcher

  // Only enable version switcher when window.versionSwitcher is filled by sphinx
  if (!window.versionSwitcher) {
    return;
  }
  let pageName = window.versionSwitcher.pageName;
  let versionJsonUrl = window.versionSwitcher.versionJsonUrl;
  let enableLocaleSupport = window.versionSwitcher.enableLocaleSupport;
  let allLocales = window.versionSwitcher.allLocales;

  // Remote version should like this.
  // .name and .alias must be unique in each locale.
  // It's not necessary to have same versions in all locales.
  // When locale is enabled, there must be only one .default=true item in each locale to indicate which one should be redirect if target version doesn't exist in target locale.

  /* 
      let allVersions = {
        "en": [
          {
            "name": "v1.2.0",
            "url": "v1.2.0",
            "alias": ["latest"],
            "default": true
          },
          {
            "name": "v1.1.0",
            "url": "v1.1.0",
            "alias": []
          },
        ],
        "zh":[
          {
            "name": "v1.0.0",
            "url": "v1.0.0",
            "alias": []
            "default": true
          },
        ],
      };
      */
  function parseCurrentURL() {
    // parseCurrentURL look up current pathname, generate all information about current version and locale.

    let pathname = window.location.pathname;

    // add "index.html" back when browser omit it.
    if (pageName.endsWith("index.html") && pathname.endsWith("/")) {
      pathname += "index.html";
    }
    if (pathname.slice(-pageName.length) !== pageName) {
      // Sphinx generated pages should have exactly same suffix
      throw 'page suffix do not match requirements';
    }

    // Get base URL by Removing '/' and pageName
    let baseURL = pathname.slice(0, -(pageName.length + 1));
    let parts = baseURL.split('/');

    let currentVersion = '';
    let currentLocale = '';

    if (enableLocaleSupport) {
      if (parts.length < 1) {
        throw 'page base URL do not have any locale information';
      }
      currentLocale = parts.pop();
    }
    if (parts.length < 1) {
      throw 'page base URL do not have any locale information';
    }
    currentVersion = parts.pop();
    // This is base URL without any version or locate.
    let globalBaseURL = parts.join('/')

    return {pageName, baseURL, currentVersion, currentLocale, globalBaseURL};
  }

  // validate Check currentLocale and currentVersion is valid.
  // Return canonicalVersion: indicate current version's real name
  function validate(allVersions, info) {
    let locale = "default";  // Use default as key when locale feature is disabled
    if (enableLocaleSupport) {
      locale = info.currentLocale;
    }
    let version_list = allVersions[locale];

    if (version_list === undefined) {
      throw `locale '${locale}'doesn't exist in remote version mapping`;
    }

    let canonicalVersion = function() {    // Match currentVersion in version_list, try to find canonical version name by matching name and alias
      for (const v of version_list) {
        if (info.currentVersion === v.name) {
          return v.name;
        }
        for (const alias_name of v.alias) {
          if (info.currentVersion === alias_name) {
            return v.name;
          }
        }
      }
      throw `version '${info.currentVersion}' doesn't exist in remove version maaping`
    }()

    return canonicalVersion;
  }

  // Set locale or version to null to indicate unchanged property.
  function constructUrl(info, targetLocale, targetVersion) {
    let segments = [info.globalBaseURL];

    if (targetLocale == null) {
      targetLocale = info.currentLocale;
    }
    if (targetVersion == null) {
      targetVersion = info.currentVersion;
    }
    segments.push(targetVersion);
    if (enableLocaleSupport) {
      segments.push(targetLocale);
    }
    segments.push(info.pageName);
    return segments.join('/') + window.location.hash;
  }

  function render(allVersions, info) {
    function onSwitchVersion(evt) {
      evt.preventDefault()
      let selected = evt.currentTarget.getAttribute('key');

      // process with alias problem, e.g. do not jump if target is just an alias of current one.
      if (selected == info.canonicalVersion) {
        // Current page is already the target version, ignore
        return;
      }

      let new_url = constructUrl(info, null, selected);
      window.location.assign(new_url);
    }

    function onSwitchLocale(evt) {
      evt.preventDefault()
      let selected = evt.currentTarget.getAttribute('key');

      let new_url = constructUrl(info, selected, null);
      window.location.assign(new_url);
    }

    // Fill the current version in the dropdown, always show real name instead of alias
    document.getElementById("version-dropdown").innerText = info.canonicalVersion;

    const menuHTML = (function() {
      return allVersions[info.currentLocale].map((version) => {
        let text = version.name;
        if (version.alias.length > 0) {
          text = `${version.name} (${version.alias.join(' ')})`
        }

        return `<button class="dropdown-item" key="${version.name}">${text}</button>`
      })
    })().join('')
    // fill the version menu
    document.getElementById("version-menu").innerHTML = menuHTML;

    // bind the changes to this menu to trigger the switching function
    $('#version-menu button').on('click', onSwitchVersion)

    // Adding locale switcher
    const localeHTML = (function() {
      return allLocales.map((l) => {
        if (l.locale === info.currentLocale) {
          return `<a class="locale-btn locale-current" key="${l.locale}">${l.display}</a>`
        } else {
          return `<a class="locale-btn locale-option "key="${l.locale}">${l.display}</a>`
        }
      })
    })().join('/')
    document.getElementById("locale-switcher").innerHTML = localeHTML;

    $('#locale-switcher .locale-option').on('click', onSwitchLocale)
  }

  // Trigger fetch as earlier as possible to speedup page loading.
  let p = fetch(versionJsonUrl).then((resp) => {
    return resp.json()
  });

  let info = parseCurrentURL();

  p.then((allVersions) => {
    let canonicalVersion = validate(allVersions, info);
    info.canonicalVersion = canonicalVersion;

    render(allVersions, info);
  })
}

$(document).ready(setupVersionSwitcher);
