import uuid

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.template import Template, Context

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Fieldset
from crispy_forms.utils import TEMPLATE_PACK, flatatt


class CollapsableFieldset(Fieldset):

    template_str = """
    <div class="accordion" id="accordion-{{ div_id }}">
      <div class="card">
        <div class="card-header" id="heading{{ div_id }}">
          <h2 class="mb-0">
            <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapse{{ div_id }}" aria-expanded="{% if collapsed %}false{% else %}true{% endif %}" aria-controls="collapseOne">
              {% if legend %}{{ legend|safe }}{% endif %}
            </button>
          </h2>
        </div>
    
        <div id="collapse{{ div_id }}" class="collapse {% if not collapsed %}show{% endif %}" aria-labelledby="heading{{ div_id }}" data-parent="#accordion-{{ div_id }}">
          <div class="card-body">
            {{ fields|safe }} 
          </div>
        </div>
      </div>
    </div>
    """

    def __init__(self, legend, *fields, **kwargs):
        self.fields = list(fields)
        self.legend = legend
        self.css_class = kwargs.pop("css_class", "")
        self.css_id = kwargs.pop("css_id", None)
        self.template = kwargs.pop("template", self.template)
        self.flat_attrs = flatatt(kwargs)
        self.collapsed = kwargs.pop('collapsed', False)

        self.div_id = kwargs.pop('div_id', None) or uuid.uuid4().hex[:6]

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        legend = ""
        if self.legend:
            legend = "%s" % Template(str(self.legend)).render(context)

        template_context = {
            "fieldset": self, "legend": legend,
            "collapsed": self.collapsed, "div_id": self.div_id,
            "fields": fields, "form_style": form_style
        }
        return Template(self.template_str).render(Context(template_context))


class UserSettingsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Contact details',
                'user_email',
                'user_phone',
                'user_phone_secondary'
            ),
            HTML('<hr/>'),
            Fieldset(
                'Email preferences',
                'daily_digest_optin',
                'weekly_digest_optin'
            ),
            HTML('<hr/>'),
            CollapsableFieldset(
                'Reset password',
                'old_password',
                'new_password',
                'confirm_password',
                collapsed=True
            ),
            ButtonHolder(
                Submit('submit', 'Save')
            )
        )

    user_email = forms.EmailField(
        required=False, max_length=200, label='Email'
    )
    user_phone = forms.CharField(required=False, max_length=150, label='Phone number')
    user_phone_secondary = forms.CharField(
        required=False, max_length=150, label='Secondary phone number'
    )

    daily_digest_optin = forms.BooleanField(
        initial=False, required=False, label='Receive daily digest email',
        help_text='Overview of any newly available actions and your in-progress actions'
    )
    weekly_digest_optin = forms.BooleanField(
        initial=False, required=False, label='Receive weekly digest email',
        help_text='Overview of new actions available and your in-progress actions'
    )

    old_password = forms.CharField(
        label='Password', required=False, max_length=100, widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label='Password', required=False, max_length=100, widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='Confirm Password', required=False, max_length=100, widget=forms.PasswordInput()
    )

    def clean(self):
        form_data = super(UserSettingsForm, self).clean()

        if form_data['old_password'] or form_data['new_password']:
            if not (form_data['old_password'] and form_data['new_password'] and form_data['confirm_password']):
                raise ValidationError('To change password you must enter all 3 fields')

            old_password_correct = self.user.check_password(
                form_data['old_password']
            )
            if not old_password_correct:
                raise ValidationError('You entered the wrong password')

            if form_data['new_password'] != form_data['confirm_password']:
                raise ValidationError('Password and confirmation did not match')

            try:
                # call django's internal password validation
                validate_password(form_data['new_password'], self.user)
            except ValidationError as err:
                msg = '\n'.join(err.messages)
                raise ValidationError(msg)

        return form_data
