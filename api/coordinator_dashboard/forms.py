import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Fieldset
from django import forms
import pytz

from actions.models import ActionV2


class AddActionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'resident',
                'help_type',
                'min_volunteers',
                'max_volunteers'
            ),
            HTML('<hr/>'),
            Fieldset(
                '', 'due_date', 'due_time',
            ),
            HTML('<hr/>'),
            Fieldset(
                '',
                'action_priority',
                'requirements',
                'public_description',
                'private_description'
            ),
            ButtonHolder(
                Submit('submit', 'Add')
            )
        )

    class Meta:
        model = ActionV2
        fields = [
            'resident',
            'help_type',
            'min_volunteers',  # todo: set widget
            'max_volunteers',
            #'due_datetime',
            'due_date',
            'due_time',
            'action_priority',
            'requirements',
            'public_description',
            'private_description'
        ]
        widgets = {
            'resident': forms.HiddenInput(),
            'requirements': forms.CheckboxSelectMultiple()
        }

    due_date = forms.CharField(
        label='Due date', required=True, max_length=10,
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    due_time = forms.CharField(
        label='Due time', required=False, initial='00:00',
        max_length=5, widget=forms.TextInput(attrs={'type': 'time'})
    )

    @staticmethod
    def _parse_due_datetime(data):

        if not data['due_date']:
            return None

        due_date = datetime.datetime.strptime(data['due_date'], '%Y-%m-%d').date()

        if data['due_time']:
            hour, minute = data['due_time'].split(':')
            due_time = datetime.time(hour=int(hour), minute=int(minute))
        else:
            due_time = datetime.time(hour=0, minute=0)

        due_datetime = datetime.datetime.combine(due_date, due_time)
        due_datetime = due_datetime.replace(tzinfo=pytz.timezone('GMT'))

        return due_datetime

    def clean(self):
        data = self.cleaned_data
        data['due_datetime'] = due_datetime = self._parse_due_datetime(data)

        if due_datetime:
            now = datetime.datetime.now().replace(tzinfo=pytz.timezone('GMT'))
            if due_datetime < now:
                raise forms.ValidationError('due date/time must be set in the future')

        return data
