from django import forms
from .models import ToDoNote
from django.core.exceptions import ValidationError


class NoteForm(forms.ModelForm):
    """
    NoteForm.
    """

    class Meta: 
        model = ToDoNote
        exclude = ('author', 'datetime_created')
