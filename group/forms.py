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
    first_end_date=forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            'type':'date'
            },
        time_attrs={
            'type':'time'
            },
        ),
        label = "1차 결과 임시 발표일"
    )

    second_end_date=forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            'type':'date'
            },
        time_attrs={
            'type':'time'
            },
        ),
        label = "2차 결과 임시 발표일"
    )

    third_end_date=forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            'type':'date'
            },
        time_attrs={
            'type':'time'
            },
        ),
        label = "3차 결과 임시 발표일"
    )

    def clean(self):
        cleaned_data = super().clean()
        first_end_date = cleaned_data.get("first_end_date")
        second_end_date = cleaned_data.get("second_end_date")
        third_end_date = cleaned_data.get("third_end_date")

        if first_end_date and second_end_date and third_end_date:
            if first_end_date < second_end_date < third_end_date:
                return cleaned_data
            else:
                raise ValidationError("시간 입력 오류")
        else:
            raise ValidationError("비어있는 칸이 있습니다.")

    class Meta:
        model = Group
        fields = ['first_end_date', 'second_end_date', 'third_end_date']


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


class VoteForm(forms.ModelForm):
    idea_vote1 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote2 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote3 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
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
        
        return cleaned_data

class FirstVoteForm(forms.ModelForm):
    idea_vote1 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote2 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote3 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote4 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote5 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote6 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote7 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote8 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote9 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    idea_vote10 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Vote
        fields = ['idea_vote1', 'idea_vote2', 'idea_vote3', 'idea_vote4', 'idea_vote5', 'idea_vote6', 'idea_vote7', 'idea_vote8', 'idea_vote9', 'idea_vote10',]

    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop('group_id', None)
        super(VoteForm, self).__init__(*args, **kwargs)
        if group_id:
            for i in range(1, 11):
                field_name = f'idea_vote{i}'
                self.fields[field_name].queryset = Idea.objects.filter(group_id=group_id)
    
    def clean(self):
        cleaned_data = super().clean()
        idea_votes = [cleaned_data.get(f"idea_vote{i}") for i in range(1, 11)]

        seen = {}

        for idea_vote in idea_votes:
            if idea_vote:
                if idea_vote in seen:
                    raise ValidationError("중복 선택 불가능")
                seen[idea_vote] = True
        
        return cleaned_data