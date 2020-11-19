// Attribute for marking a field as edited
const ATTR_EDITED = 'data-edited';

(function () {
  // Wait for everything to be loaded, especially jQuery
  document.addEventListener('DOMContentLoaded', () => {
    if (window.django) {
      const $ = window.django.jQuery;
      const data = getData(); // Read the data passed by the backend

      setupUserAjaxUrl($, data);

      // Wait until all Django related setup code has run
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
  const element = document.getElementById('js-data');
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
  
    $(document).on('change', '[name="help_type"]', function ({ target }) {
      const defaultRequirements = data.action_requirements_for_help_types[target.value] || [];
     
      // Clear the selected options, using Django's SelectBox API
      // as there is some caching behind the scene that breaks if 
      // moving only the HTML elements
      window.SelectBox.move_all('id_requirements_to','id_requirements_from')

      // We need to grab the list of options each time, 
      // looks like elements are re-created by the move_all
      const options = $('.field-requirements option').toArray();
      for (option of options) {
        // Mark options as selected as needed by the help type requirements
        option.selected = defaultRequirements.indexOf(parseInt(option.value)) != -1
      }
    
      // And move the selected options to the selected box
      window.SelectBox.move('id_requirements_from','id_requirements_to')
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
    $(document).on('change', '[name="help_type"]', function ({ target }) {
      const templates = data.action_description_templates[target.value] || {};

      // Loop through the fields that we have templates for.
      ['public', 'private'].forEach((descriptionType) => {
        const $field = $(`[name="${descriptionType}_description"]`);
        const descriptionTemplate = templates[`${descriptionType}_description_template`]
        const currentDescription = ($field.val() || "").trim();

        // If the current description is empty or is the template, we can update it.
        if (!currentDescription || !$field[0].hasAttribute('data-edited')) {
          $field.val(descriptionTemplate)
          $field.removeAttr('data-edited');
        }

      })

      currentHelpType = target.value;
    })

    // Track editions of descriptions to prevent replacement of edited value
    $(document).on('input', '[name="public_description"],[name="private_description"]', function ({ target }) {
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
  let submitted;
  $(document).on('submit', function () {
    submitted = true;
  });
  $(document).one('change', function () {
    window.addEventListener('beforeunload', (event) => {
      if (!submitted) {
        // Cancel the event as stated by the standard.
        event.preventDefault();
        // Chrome requires returnValue to be set.
        event.returnValue = '';
        return `Looks like you've edited some data and not saved it yet. If you navigate away, you'll lose those changes. 
        
        Are you sure you want to continue?
        `
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
  setUserFieldPlaceholder($);

  // Unchecks the "user_without_account" when picking an account in the list of users
  $(document).on('change', '[name="user"]', function ({ target }) {
    if (target.value) {
      $('[name="user_without_account"]')
        .prop('checked', false)
        .trigger('change');

    }
  });
}

function setupUserAjaxUrl($, { profile_type, profile_id }) {
  if (profile_type) {
    const url = $('[name="user"]').data('ajax--url');
    if (url) {
      let new_url = `${url}?without_profile_type=${profile_type}`
      if (profile_id) {
        new_url = `${new_url}&profile_id=${profile_id}`
      }
      $('[name="user"').data('ajax--url', new_url)
    }
  }
}

function setUserFieldPlaceholder($) {
  const placeholder = getPlaceholder($);
  // Use jQuery's `data` rather than set the attribute
  // as the attribute wouldn't get read
  $('[name="user"]').data('placeholder', placeholder);
  $('[name="user"]').select2({ placeholder });
}

function getPlaceholder($) {
  if ($('[name="user_without_account"]').prop('checked')) {
    return 'No account required';
  } else {
    return 'Automatically create a new account';
  }
}
