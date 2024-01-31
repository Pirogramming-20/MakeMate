from django import forms
from .models import Group

class GroupBaseForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'team_number', 'password']