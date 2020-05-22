from django.forms import ModelForm, BooleanField
from crispy_forms.helper import FormHelper
from .models import Action, ActionStatus
from django.utils.translation import ugettext_lazy as _


class ActionFeedbackForm(ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Set up CrispyForm
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    # Customize which fields will get rendered
    class Meta:
        model = Action
        fields = ['time_taken', 'notes']
        # Customize labels and help texts
        labels = {
            'time_taken': _("How long did it take?"),
            'notes': _("Any particular feedback?"),
        }

        # Override some unnecessary help texts as labels are meaningful enough
        help_texts = {
            'time_taken': None,
            'notes': None
        }
    # And add form specific fields
    will_be_ongoing = BooleanField(
        required=False, label=_("I've scheduled with the person to help them recurrently"))

    def save(self, commit=True):
        self.instance.action_status = ActionStatus.COMPLETED
        super().save()
