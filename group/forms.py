from django import forms
from .models import Group

class GroupBaseForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'team_number', 'password', 'type']

class GroupDetailForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'ability_description1',
            'ability_description2',
            'ability_description3',
            'ability_description4',
            'ability_description5',
            'choice',
            'tech_stack',
        ]

class GroupDateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['end_date',]