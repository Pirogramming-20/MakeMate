from django import forms
from django.core.exceptions import ValidationError
from apps.group.models import Group, MemberState, Idea, Vote 
from django.contrib.admin import widgets 

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