from django import forms

CHOICES = (
    ('Candidate 1', 'Candidate 1'),
    ('Candidate 2', 'Candidate 2'),
    ('Candidate 3', 'Candidate 3'),
)

class VoteForm(forms.Form):
    vote = forms.ChoiceField(label ="",required=True,widget=forms.RadioSelect, choices=CHOICES)