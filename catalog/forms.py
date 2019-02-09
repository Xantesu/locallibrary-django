from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):

    renewal_date = forms.DateField(help_text='Enter a date between now an 4 weeks (default 3 weeks).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check if date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date in in the allowed range
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal date more than 4 weeks ahead'))

        return data