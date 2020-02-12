/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/theme.js":
/*!*************************!*\
  !*** ./src/js/theme.js ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("/*** IMPORTS FROM imports-loader ***/\n(function() {\n\nalert('hi from webpack')\n\n// TOC sidebar - add \"active\" class to parent list\n//\n// Bootstrap's scrollspy adds the active class to the <a> link,\n// but for the automatic collapsing we need this on the parent list item.\n//\n// The event is triggered on \"window\" (and not the nav item as documented),\n// see https://github.com/twbs/bootstrap/issues/20086\n$(window).on('activate.bs.scrollspy', function() {\n  var navLinks = document.querySelectorAll('#bd-toc-nav a');\n  for (var i = 0; i < navLinks.length; i++) {\n    var navLink = navLinks[i];\n    navLink.parentElement.classList.remove('active');\n  }\n  var navLinks = document.querySelectorAll('#bd-toc-nav a.active');\n  for (var i = 0; i < navLinks.length; i++) {\n    var navLink = navLinks[i];\n    navLink.parentElement.classList.add('active');\n  }\n});\n\n/**\n * Use left and right arrow keys to navigate forward and backwards.\n */\nconst LEFT_ARROW_KEYCODE = 37;\nconst RIGHT_ARROW_KEYCODE = 39;\n\nconst getPrevUrl = () => document.getElementById('prev-link').href;\nconst getNextUrl = () => document.getElementById('next-link').href;\nconst initPageNav = event => {\n  const keycode = event.which;\n\n  if (keycode === LEFT_ARROW_KEYCODE) {\n    window.location.href = getPrevUrl();\n  } else if (keycode === RIGHT_ARROW_KEYCODE) {\n    window.location.href = getNextUrl();\n  }\n};\n\nvar keyboardListener = false;\n$(document).ready(() => {\n  if (keyboardListener === false) {\n    document.addEventListener('keydown', initPageNav);\n    keyboardListener = true;\n  }\n});\n\n}.call(window));\n\n//# sourceURL=webpack:///./src/js/theme.js?");

/***/ }),

/***/ "./src/scss/theme.scss":
/*!*****************************!*\
  !*** ./src/scss/theme.scss ***!
  \*****************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony default export */ __webpack_exports__[\"default\"] = (__webpack_require__.p + \"css/theme.css\");\n\n//# sourceURL=webpack:///./src/scss/theme.scss?");

/***/ }),

/***/ 0:
/*!*****************************************************!*\
  !*** multi ./src/js/theme.js ./src/scss/theme.scss ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("__webpack_require__(/*! ./src/js/theme.js */\"./src/js/theme.js\");\nmodule.exports = __webpack_require__(/*! ./src/scss/theme.scss */\"./src/scss/theme.scss\");\n\n\n//# sourceURL=webpack:///multi_./src/js/theme.js_./src/scss/theme.scss?");

/***/ })

/******/ });