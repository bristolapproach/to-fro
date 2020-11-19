// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles
parcelRequire = (function (modules, cache, entry, globalName) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports, this);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [function (require, module) {
      module.exports = exports;
    }, {}];
  };

  var error;
  for (var i = 0; i < entry.length; i++) {
    try {
      newRequire(entry[i]);
    } catch (e) {
      // Save first error but execute all entries
      if (!error) {
        error = e;
      }
    }
  }

  if (entry.length) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(entry[entry.length - 1]);

    // CommonJS
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = mainExports;

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
     define(function () {
       return mainExports;
     });

    // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }

  // Override the current require with this new one
  parcelRequire = newRequire;

  if (error) {
    // throw error from earlier, _after updating parcelRequire_
    throw error;
  }

  return newRequire;
})({"sfHE":[function(require,module,exports) {
function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

// Attribute for marking a field as edited
var ATTR_EDITED = 'data-edited';

(function () {
  // Wait for everything to be loaded, especially jQuery
  document.addEventListener('DOMContentLoaded', function () {
    if (window.django) {
      var $ = window.django.jQuery;
      var data = getData(); // Read the data passed by the backend

      setupUserAjaxUrl($, data); // Wait until all Django related setup code has run
      // so we don't respond to synthetic change events triggered
      // during their initialization

      $(function () {
        setupActionDescriptionTemplates($, data);
        setupHelpTypeDefaultRequirements($, data);
        setupUserAccountsBehaviour($);
        setupConfirmNavigationIfEdited($);
      });
    }
  });
})();

function getData() {
  var element = document.getElementById('js-data');

  if (element) {
    return JSON.parse(element.innerText);
  }

  return {};
}
/**
 * Manages the pre-filling of requirements according
 * to the default requirements associated to the selected help type
 * @param {jQuery} $ 
 * @param {Object} data 
 */


function setupHelpTypeDefaultRequirements($, data) {
  if (data.action_requirements_for_help_types) {
    $(document).on('change', '[name="help_type"]', function (_ref) {
      var target = _ref.target;
      var defaultRequirements = data.action_requirements_for_help_types[target.value] || []; // Clear the selected options, using Django's SelectBox API
      // as there is some caching behind the scene that breaks if 
      // moving only the HTML elements

      window.SelectBox.move_all('id_requirements_to', 'id_requirements_from'); // We need to grab the list of options each time, 
      // looks like elements are re-created by the move_all

      var options = $('.field-requirements option').toArray();

      var _iterator = _createForOfIteratorHelper(options),
          _step;

      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          option = _step.value;
          // Mark options as selected as needed by the help type requirements
          option.selected = defaultRequirements.indexOf(parseInt(option.value)) != -1;
        } // And move the selected options to the selected box

      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }

      window.SelectBox.move('id_requirements_from', 'id_requirements_to');
    });
  }
}
/**
 * Manages the prefilling of action descriptions according
 * to the templates corrsponding to the selecte help type
 * @param {jQuery} $ 
 * @param {Object} data - The hash of data passed to the view
 */


function setupActionDescriptionTemplates($, data) {
  if (data.action_description_templates) {
    $(document).on('change', '[name="help_type"]', function (_ref2) {
      var target = _ref2.target;
      var templates = data.action_description_templates[target.value] || {}; // Loop through the fields that we have templates for.

      ['public', 'private'].forEach(function (descriptionType) {
        var $field = $("[name=\"".concat(descriptionType, "_description\"]"));
        var descriptionTemplate = templates["".concat(descriptionType, "_description_template")];
        var currentDescription = ($field.val() || "").trim(); // If the current description is empty or is the template, we can update it.

        if (!currentDescription || !$field[0].hasAttribute('data-edited')) {
          $field.val(descriptionTemplate);
          $field.removeAttr('data-edited');
        }
      });
      currentHelpType = target.value;
    }); // Track editions of descriptions to prevent replacement of edited value

    $(document).on('input', '[name="public_description"],[name="private_description"]', function (_ref3) {
      var target = _ref3.target;
      target.setAttribute('data-edited', '');
    });
  }
}
/**
 * Adds a confirmation before navigation if users
 * have edited anything on the page
 * @param {jQuery} $ 
 */


function setupConfirmNavigationIfEdited($) {
  var submitted;
  $(document).on('submit', function () {
    submitted = true;
  });
  $(document).one('change', function () {
    window.addEventListener('beforeunload', function (event) {
      if (!submitted) {
        // Cancel the event as stated by the standard.
        event.preventDefault(); // Chrome requires returnValue to be set.

        event.returnValue = '';
        return "Looks like you've edited some data and not saved it yet. If you navigate away, you'll lose those changes. \n        \n        Are you sure you want to continue?\n        ";
      }
    });
  });
}
/**
 * Manages the user account fields in the volunteer and coordinator
 * forms
 * @param {jQuery} $ 
 */


function setupUserAccountsBehaviour($) {
  // Controls which placeholder is shown, depending on whether an account is needed
  // or not
  $(document).on('change', '[name="user_without_account"]', function () {
    setUserFieldPlaceholder($);
  });
  setUserFieldPlaceholder($); // Unchecks the "user_without_account" when picking an account in the list of users

  $(document).on('change', '[name="user"]', function (_ref4) {
    var target = _ref4.target;

    if (target.value) {
      $('[name="user_without_account"]').prop('checked', false).trigger('change');
    }
  });
}

function setupUserAjaxUrl($, _ref5) {
  var profile_type = _ref5.profile_type,
      profile_id = _ref5.profile_id;

  if (profile_type) {
    var url = $('[name="user"]').data('ajax--url');

    if (url) {
      var new_url = "".concat(url, "?without_profile_type=").concat(profile_type);

      if (profile_id) {
        new_url = "".concat(new_url, "&profile_id=").concat(profile_id);
      }

      $('[name="user"').data('ajax--url', new_url);
    }
  }
}

function setUserFieldPlaceholder($) {
  var placeholder = getPlaceholder($); // Use jQuery's `data` rather than set the attribute
  // as the attribute wouldn't get read

  $('[name="user"]').data('placeholder', placeholder);
  $('[name="user"]').select2({
    placeholder: placeholder
  });
}

function getPlaceholder($) {
  if ($('[name="user_without_account"]').prop('checked')) {
    return 'No account required';
  } else {
    return 'Automatically create a new account';
  }
}
},{}]},{},["sfHE"], null)
//# sourceMappingURL=admin.js.map