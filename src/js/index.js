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
import { name, part } from 'file-loader';

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

function parseCurrentURL(switchers_enable) {
  // parseCurrentURL look up current pathname, generate current version locale

  let pathname = window.location.pathname;
  let pageName = window.switcher.pageName;

  // add "index.html" back when browser omit it.
  if (pageName.endsWith("index.html") && pathname.endsWith("/")) {
    pathname += "index.html";
  }
  if (pathname.slice(-pageName.length) !== pageName) {
    // Sphinx generated pages should have exactly same suffix
    throw 'page suffix do not match requirements'
  }

  let baseURL = pathname.slice(0, -(pageName.length + 1));
  let parts = baseURL.split("/");
  let switcherInfo = {};
  // find switcher info
  for(let switchidx=0; switchidx<switchers_enable.length; switchidx++) {
    let switchName = switchers_enable[switchidx];
    switcherInfo[switchName+"HeadURL"] = parts.slice(0,parts.length-switchidx-1).join('/');
    switcherInfo[switchName+"URL"] = parts[parts.length-switchidx-1];
    if(switchidx===0) {
      switcherInfo[switchName+"TailURL"] = pageName
    } else {
      switcherInfo[switchName+"TailURL"] = parts.slice(parts.length-switchidx).join('/')+"/"+pageName;
    }
  }
  
  return switcherInfo
}

function setupVersionSwitcher(allVersions, versionHeadURL, versionURL, versionTailURL) {
  // Setup Version Switcher

  // version switcher's config should be a (key, value) pair of config.json:
  // 'items' is a list of all versions. `name` and `labels` must be unique.
  // You should specify a default version(both name and labels are ok).
  /* 
      let configs = {
          "items": [
              {
                  "name": "v1.0",
                  "url": "1.0",
                  "labels": []
              },
              {
                  "name": "v1.3",
                  "url": "1.3",
                  "labels": ["stable"]
              },
              {
                  "name": "v1.4",
                  "url": "1.4",
                  "labels": ["latest"]
              },
          ],
          "default": "stable"
      }
  */
  

  // validate Check currentVersion is valid.
  // Return canonicalVersion: indicate current version's real url
  function validate(allVersions, versionURL) {
    for(const version of allVersions.items) {
      if((version.url === versionURL) || (version.name === versionURL)) {
        return version
      }
      for(const label of version.labels) {
        if(label === versionURL) {
          return version
        }
      }
    }

    throw `version '${versionURL}' doesn't exist in remove version mapping`
  }

  function render(allVersions, info) {
    function onSwitchVersion(evt) {
      evt.preventDefault()
      let selected = evt.currentTarget.getAttribute('key');

      // process with alias problem, e.g. do not jump if target is just an alias of current one.
      if (selected == info.currentVersion.url) {
        // Current page is already the target version, ignore
        return;
      }

      let new_url = info.versionHeadURL+"/"+selected+"/"+info.versionTailURL;
      window.location.assign(new_url);
    }

    // Fill the current version in the dropdown, always show real name instead of alias
    document.getElementById("version-dropdown").innerText = info.currentVersion.name;

    const menuHTML = (function() {
      return allVersions.items.map((version) => {
        let text = version.name;
        if (version.labels.length > 0) {
          text = `${version.name} (${version.labels.join(' ')})`
        }

        return `<button class="dropdown-item" key="${version.url}">${text}</button>`
      })
    })().join('')
    // fill the version menu
    document.getElementById("version-menu").innerHTML = menuHTML;

    // bind the changes to this menu to trigger the switching function
    $('#version-menu button').on('click', onSwitchVersion)
  }

  let currentVersion = validate(allVersions, versionURL);
  let info = {versionHeadURL, versionURL, versionTailURL, currentVersion}
  render(allVersions, info)
}

function applyConfig() {
  let switchers_enable = window.switcher.switchers;

  if(switchers_enable.length === 0) return;

  let configUrl = window.configUrl;
  fetch(configUrl).then((resp) => {
    return resp.json()
  }).then((configs) => {
    let info = parseCurrentURL(switchers_enable);
    
    if(switchers_enable.indexOf("version") !== -1) {
      // enable version switcher
      setupVersionSwitcher(configs["version"], info.versionHeadURL, info.versionURL, info.versionTailURL)
    }
  }).catch((error) => {
    throwBtnError("version-dropdown", error)
  })
}

function throwBtnError(btnID, errMsg) {
  $("#"+btnID).addClass("btn-danger").prop("disabled", true).text("Error!!!");
  throw errMsg
}

$(document).ready(() => {
  scrollToActive();
  addTOCInteractivity();
  applyConfig();
});