from datetime import date

from django.forms import ModelForm

from spendtrackapp.models import Entry, Plan


class EntryForm(ModelForm):
    """Form to validate entry info"""

    class Meta:
        model = Entry
        fields = ['date', 'content', 'value']  # category_id is validated manually

    # def _post_clean(self):
    #     super()._post_clean()
    #
    #     # validate category_id
    #     if 'category_id' not in self.data:
    #         self.add_error('category_id', 'Missing category')
    #     else:
    #         category_id = self.data['category_id']
    #         category = Category.get_leaf_category(category_id)
    #         if category is None:
    #             self.add_error('category_id', 'Invalid category')


class PlanForm(ModelForm):
    """Form to validate plan info"""

    class Meta:
        model = Plan
        fields = ['name', 'start_date', 'end_date',
                  'planned_total', 'compare', 'category']

    def _post_clean(self):
        super()._post_clean()

        # validate dates
        if 'start_date' in self.cleaned_data and 'end_date' in self.cleaned_data:
            start_date = self.data['start_date']
            end_date = self.data['end_date']

            # start_date must <= end_date
            if start_date > end_date:
                self.add_error('end_date', 'End date must be after start date')

            # start date can't be in the past
            if start_date < date.today().isoformat():
                self.add_error('start_date', 'Start date cannot be in the past')

        # validate planned_total
        if 'planned_total' in self.cleaned_data:
            planned_total = float(self.data['planned_total'])
            if planned_total <= 0:
                self.add_error('planned_total', 'Total must be positive')
