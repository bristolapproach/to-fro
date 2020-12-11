from django.forms import ModelForm, BooleanField, MultiWidget, NumberInput, Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Action, ActionStatus, ActionFeedback
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _

import logging
logger = logging.getLogger(__name__)


class SplitDuration(MultiWidget):
    """
    Custom widget for the input of durations
    as a NumberInput for the hours and a Select
    for the minutes
    """

    template_name = "forms/split_duration.html"

    def __init__(self, legend=None, default_hours=0, default_minutes=15, attrs=None):
        hours = [(v, v) for v in (0, 1, 2, 3, 4, 5)]
        minutes = [(v, v) for v in (0, 15, 30, 45)]
        widgets = [
            Select(attrs=attrs, choices=hours),
            Select(attrs=attrs, choices=minutes)
        ]
        self.legend = legend
        self.default_hours = default_hours
        self.default_minutes = default_minutes
        super().__init__(widgets, attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Prepare some classes for rendering
        context['widget']['subwidgets'][0]['attrs']['class'] += " custom-select text-right"
        context['widget']['subwidgets'][1]['attrs']['class'] += " custom-select text-right"

        context.update({
            'legend': self.legend
        })
        return context

    def decompress(self, value):
        if (isinstance(value, timedelta)):
            return [value.hours, value.minutes]
        elif (isinstance(value, str)):
            hours, minutes, seconds = value.split(':')
            # Remove leading 0 for the hours, as we don't
            # want to lead users into unnecessary input
            return [int(hours or 0), int(minutes or 0)]
        return [self.default_hours, self.default_minutes]

    def value_from_datadict(self, data, files, name):
        hours, minutes = super().value_from_datadict(data, files, name)
        return '{:02d}:{:02d}:{:02d}'.format(int(hours or 0), int(minutes or 0), 0)


class ActionFeedbackForm(ModelForm):

    layout = Layout(
        Field('notes'),
        Field('will_be_ongoing'),
        Field('time_taken')
    )

    def __init__(self, *args, **kwargs):
        """
        Set up CrispyForm
        """
        self.action = kwargs.pop('action')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = self.layout

    # Customize which fields will get rendered
    class Meta:
        model = ActionFeedback
        widgets = {
            'time_taken': SplitDuration(legend=_("How long did it take?"))
        }
        fields = ['time_taken', 'notes']
        # Customize labels and help texts
        labels = {
            # Label is set by the legend of the SplitDuration
            'time_taken': '',
            'notes': _("Any particular feedback?"),
        }

        # Override some unnecessary help texts as labels are meaningful enough
        help_texts = {
            'time_taken': None,
            'notes': None
        }

    # And add form specific fields
    will_be_ongoing = BooleanField(
        required=False, label=_("I've scheduled with the person to help them regularly"))

    def get_initial_for_field(self, field, field_name):
        initial = super().get_initial_for_field(field, field_name)
        if (field_name == 'will_be_ongoing'):
            return self.action.action_status == ActionStatus.ONGOING
        return initial

    def save(self, commit=True):
        # Create the feedback instance.
        self.instance.notes = self.cleaned_data['notes']
        self.instance.time_taken = self.cleaned_data['time_taken']

        # Set a new ActionStatus.
        if self.cleaned_data.get('will_be_ongoing'):
            self.action.action_status = ActionStatus.ONGOING
        else:
            self.action.action_status = ActionStatus.COMPLETED
        self.action.save()
        super().save()


class ActionCancellationForm(ActionFeedbackForm):

    layout = Layout(
        Field('notes'),
        Field('time_taken')
    )
    will_be_ongoing = None

    class Meta(ActionFeedbackForm.Meta):
        widgets = {
            'time_taken': SplitDuration(legend=_("Did it take up any of your time?"), default_minutes=0)
        }
        labels = {
            # Label is set by the legend of the SplitDuration
            'time_taken': '',
            'notes': _("What's happening?"),
        }
