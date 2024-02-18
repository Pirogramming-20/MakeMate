from django import forms
from apps.group.models import Group, MemberState

class GroupPasswordForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['password']

class NonAdminInfoForm(forms.ModelForm):
    class Meta:
        model = MemberState
        fields = ['group_ability']

class GroupBaseForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label = "비밀번호"
    )
    class Meta:
        model = Group
        fields = ['title', 'password']

class GroupDetailForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'ability_description1',
            'ability_description2',
            'ability_description3',
            'ability_description4',
            'ability_description5',
        ]


class GroupDateForm(forms.ModelForm):
    end_date=forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            'type':'date'
            },
        time_attrs={
            'type':'time'
            },
        ),
        label = "결과 임시 발표일"
    )

    class Meta:
        model = Group
        fields = ['end_date']
