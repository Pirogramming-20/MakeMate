from django import forms
from django.core.exceptions import ValidationError
from .models import Group, MemberState, Idea, Vote 
from django.contrib.admin import widgets 

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
        help_texts = {
            'intro': '50자 미만으로 작성해주세요.',
        }


class VoteForm(forms.ModelForm):
    idea_vote1 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
    idea_vote2 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
    idea_vote3 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Vote
        fields = ['idea_vote1', 'idea_vote2', 'idea_vote3']
    
    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop('group_id', None)
        super(VoteForm, self).__init__(*args, **kwargs)
        if group_id:
            self.fields['idea_vote1'].queryset = Idea.objects.filter(group_id=group_id)
            self.fields['idea_vote2'].queryset = Idea.objects.filter(group_id=group_id)
            self.fields['idea_vote3'].queryset = Idea.objects.filter(group_id=group_id)

    def clean(self):
        cleaned_data = super().clean()
        idea_vote1 = cleaned_data.get("idea_vote1")
        idea_vote2 = cleaned_data.get("idea_vote2")
        idea_vote3 = cleaned_data.get("idea_vote3")

        # 중복 검사
        if idea_vote1 and idea_vote2 and idea_vote1 == idea_vote2:
            raise ValidationError("중복 선택 불가능")
        if idea_vote2 and idea_vote3 and idea_vote2 == idea_vote3:
            raise ValidationError("중복 선택 불가능")
        if idea_vote1 and idea_vote3 and idea_vote1 == idea_vote3:
            raise ValidationError("중복 선택 불가능")
        
        if not idea_vote1 or not idea_vote2 or not idea_vote3:
            raise ValidationError("모든 지망을 선택해야 합니다.")
        
        return cleaned_data
