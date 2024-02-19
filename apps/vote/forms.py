from django import forms
from django.core.exceptions import ValidationError
from apps.group.models import Idea, Vote  

class VoteForm(forms.ModelForm):
    idea_vote1 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )
    idea_vote2 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )
    idea_vote3 = forms.ModelChoiceField(
        queryset=Idea.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )

    class Meta:
        model = Vote
        fields = ["idea_vote1", "idea_vote2", "idea_vote3"]

    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop("group_id", None)
        super(VoteForm, self).__init__(*args, **kwargs)
        if group_id:
            self.fields["idea_vote1"].queryset = Idea.objects.filter(
                group_id=group_id)
            self.fields["idea_vote2"].queryset = Idea.objects.filter(
                group_id=group_id)
            self.fields["idea_vote3"].queryset = Idea.objects.filter(
                group_id=group_id)

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
