// Attribute for marking a field as edited
const ATTR_EDITED = 'data-edited';

(function () {
  // Wait for everything to be loaded, especially jQuery
  document.addEventListener('DOMContentLoaded', () => {
    const $ = window.django.jQuery;
    const data = getData(); // Read the data passed by the backend

    if (data.job_description_templates) {
      // Wait until all Django related setup code has run
      // so we don't respond to synthetic change events triggered
      // during their initialization
      $(function () {
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
