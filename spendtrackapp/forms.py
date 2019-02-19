from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm, Form, ChoiceField, IntegerField, DateField, EmailField

from spendtrackapp.models import Entry, Plan, Category
from spendtrackapp.urls.converters import *
from spendtrackapp.views.utils import is_valid_iso_week


##############################################################
#                          FIELDS                            #
##############################################################

class NullableIntegerField(IntegerField):
    """An integer field that can be empty"""

    def clean(self, value):
        return super(IntegerField, self).clean(value) if value else None


class NullableDateField(DateField):
    """A date filed that can be empty"""

    def clean(self, value):
        return super(DateField, self).clean(value) if value else None


##############################################################
#                          FORMS                             #
##############################################################

class EntryForm(ModelForm):
    """Form to validate entry info"""

    class Meta:
        model = Entry
        fields = ['date', 'content', 'value', 'leaf_category', 'user']

    def clean(self):
        super().clean()

        # validate leaf category
        if 'leaf_category' not in self.errors:
            leaf_category_id = self.data['leaf_category']
            category = Category.get_leaf_category(leaf_category_id)
            if category is None:
                self.add_error('leaf_category', 'Invalid category')

        return self.cleaned_data

    def save(self, commit=True):
        super().save(commit)

        # set the list of categories after saving entry to database
        if commit:
            leaf_category = Category.get_leaf_category(self.instance.leaf_category_id)
            if leaf_category is None:
                raise ValueError('Invalid leaf category')
            self.instance.change_category(leaf_category)

        return self.instance


class PlanForm(ModelForm):
    """Form to validate plan info"""

    class Meta:
        model = Plan
        fields = ['name', 'start_date', 'end_date',
                  'planned_total', 'compare', 'category', 'user']

    def clean(self):
        super().clean()

        # validate dates
        if 'start_date' in self.cleaned_data and 'end_date' in self.cleaned_data:
            start_date = self.data['start_date']
            end_date = self.data['end_date']

            # start_date must <= end_date
            if start_date > end_date:
                self.add_error('end_date', 'End date must be after start date')

            # start date can't be in the past
            # if start_date < date.today().isoformat():
            #     self.add_error('start_date', 'Start date cannot be in the past')

        # validate planned_total
        if 'planned_total' in self.cleaned_data:
            planned_total = float(self.data['planned_total'])
            if planned_total <= 0:
                self.add_error('planned_total', 'Total must be positive')

        return self.cleaned_data


class SearchTimeForm(Form):
    """Form to validate search time queries"""

    search_type = ChoiceField(choices=[
        ['year', 'year'], ['month', 'month'], ['week', 'week'], ['date_range', 'date_range']
    ])
    year = NullableIntegerField(min_value=1000, max_value=9999)
    month = NullableIntegerField(min_value=1, max_value=12)
    week = NullableIntegerField(min_value=1, max_value=53)
    start_date = NullableDateField()
    end_date = NullableDateField()

    def clean(self):
        super().clean()

        # check that required fields according to 'search_type' are present
        if 'search_type' in self.cleaned_data:

            search_type = self.data['search_type']
            year = self.cleaned_data.get('year', None)
            month = self.cleaned_data.get('month', None)
            week = self.cleaned_data.get('week', None)
            start_date = self.cleaned_data.get('start_date', None)
            end_date = self.cleaned_data.get('end_date', None)

            if search_type == 'year' and year is None:
                self.add_error('year', 'This field is required.')

            elif search_type == 'month':
                if year is None:
                    self.add_error('year', 'This field is required.')
                if month is None:
                    self.add_error('month', 'This field is required.')

            elif search_type == 'week':
                if year is None:
                    self.add_error('year', 'This field is required.')
                if week is None:
                    self.add_error('week', 'This field is required.')
                if None not in [year, week] and not is_valid_iso_week(year, week):
                    self.add_error('week', 'Invalid ISO week')

            elif search_type == 'date_range':
                if start_date is None:
                    self.add_error('start_date', 'This field is required.')
                if end_date is None:
                    self.add_error('end_date', 'This field is required.')
                if None not in [start_date, end_date] and start_date > end_date:
                    self.add_error('end_date', 'End date must come after start date.')

        return self.cleaned_data

    _relevant_data_str = None

    @property
    # TODO consider make this a immutable dict
    def relevant_data_str(self):
        """Return a dictionary contains strings of relevant data to the search type"""

        # raise error when data is not clean
        if not self.is_valid():
            raise ValueError('Data is not clean')

        if self._relevant_data_str is None:
            search_type = self.cleaned_data['search_type']

            if search_type == 'year':
                year_converter = FourDigitYearConverter()
                self._relevant_data_str = {
                    'year': year_converter.to_url(self.cleaned_data['year'])
                }
            elif search_type == 'month':
                year_converter = FourDigitYearConverter()
                month_converter = ThreeCharMonthConverter()
                self._relevant_data_str = {
                    'year': year_converter.to_url(self.cleaned_data['year']),
                    'month': month_converter.to_url(self.cleaned_data['month'])
                }
            elif search_type == 'week':
                year_converter = FourDigitYearConverter()
                week_converter = TwoDigitWeekConverter()
                self._relevant_data_str = {
                    'year': year_converter.to_url(self.cleaned_data['year']),
                    'week': week_converter.to_url(self.cleaned_data['week'])
                }
            else:
                date_converter = DateConverter()
                self._relevant_data_str = {
                    'start_date': date_converter.to_url(self.cleaned_data['start_date']),
                    'end_date': date_converter.to_url(self.cleaned_data['end_date'])
                }

        return self._relevant_data_str


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        super().clean()

        if 'email' in self.data and self.data['email'].strip() == '':
            self.add_error('email', 'Email cannot be empty.')

        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    def clean(self):
        super().clean()

        if self.errors == {}:
            try:
                self.user = User.objects.get(email=self.cleaned_data['email'])
            except User.DoesNotExist:
                self.add_error('email', 'Invalid email')


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField, 'email': EmailField}

    def clean(self):
        super().clean()
        if 'email' in self.cleaned_data and self.cleaned_data['email'] == '':
            self.add_error('email', 'Email cannot be empty')
        return self.cleaned_data
