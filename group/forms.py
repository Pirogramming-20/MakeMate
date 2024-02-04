from django import forms
from .models import Group, MemberState, Idea
from django.contrib.admin import widgets 

class GroupPasswordForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['password']

class NonAdminInfoForm(forms.ModelForm):
    class Meta:
        model = MemberState
        fields = ['group_ability', 'group_tech_stack']

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

# class GroupDateForm(forms.ModelForm):
#     end_date = forms.DateField(widget = forms.SelectDateWidget)
#     class Meta:
#         model = Group
#         fields = ['end_date',]

class GroupDateForm(forms.ModelForm):
    end_date=forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            'type':'date'
            },
        time_attrs={
            'type':'time'
            },
        )
    )

    class Meta:
        model = Group
        fields = ['end_date']

# class GroupForm(forms.ModelForm):
#     class Meta():
#         model = Group
#         fields = ('__all__')
#         labels = {
            
#         }

class IdeaForm(forms.ModelForm):
    class Meta():
        model = Idea
        fields = ('title', 'intro', 'file', 'content')
        labels = {
            'title': '제목', 
            'intro': '한 줄 소개',
            'file': '첨부파일', 
            'content': '내용',
        }
