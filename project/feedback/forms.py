from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['response', 'rating']

        labels = {
            'response': 'Feedback Response',
            'rating': 'Rate the Service',
        }

        widgets = {
            'response': forms.Textarea(attrs={'required': True, 'class': 'response'}),
            'rating': forms.RadioSelect(attrs={'required': False}, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        }


    def clean_response(self):
        response = self.cleaned_data['response']
        if len(response) > 4096:
            raise ValidationError('Response cannot be longer than 4096 bytes.')
        if strip_tags(response) != response:
            return strip_tags(response)
        else:
            return response
