from django.forms import ModelForm

from .models import Entry


class EntryForm(ModelForm):
    """Form to validate entry info"""

    class Meta:
        model = Entry
        fields = ['date', 'content', 'value']  # category_id is validate manually
