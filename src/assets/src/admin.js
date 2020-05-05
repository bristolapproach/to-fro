// Attribute for marking a field as edited
const ATTR_EDITED = 'data-edited';

(function () {
  // Wait for everything to be loaded, especially jQuery
  document.addEventListener('DOMContentLoaded', () => {
    const $ = window.django.jQuery;
    const data = getData(); // Read the data passed by the backend


    // Wait until all Django related setup code has run
    // so we don't respond to synthetic change events triggered
    // during their initialization
    $(function () {
      setupJobDescriptionTemplates($, data);
      setupUserAccountsBehaviour($);
    });
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
 * Manages the prefilling of job descriptions according
 * to the templates corrsponding to the selecte help type
 * @param {jQuery} $ 
 * @param {Object} data - The hash of data passed to the view
 */
function setupJobDescriptionTemplates($, data) {
  if (data.job_description_templates) {
    $(document).on('change', '[name="help_type"]', function ({ target }) {
      const templates = data.job_description_templates[target.value] || {};

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
