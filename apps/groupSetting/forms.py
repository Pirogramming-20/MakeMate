from django import forms
from django.core.exceptions import ValidationError
from apps.group.models import Group, MemberState, Idea


class GroupPasswordForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["password"]


class NonAdminInfoForm(forms.ModelForm):
    class Meta:
        model = MemberState
        fields = ["group_ability"]


class GroupBaseForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")

    class Meta:
        model = Group
        fields = ["title", "password"]


class GroupDetailForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            "ability_description1",
            "ability_description2",
            "ability_description3",
            "ability_description4",
            "ability_description5",
        ]


class GroupDateForm(forms.ModelForm):
    first_end_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            time_attrs={"type": "time"},
        ),
        label="1차 결과 임시 발표일",
    )

    second_end_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            time_attrs={"type": "time"},
        ),
        label="2차 결과 임시 발표일",
    )

    third_end_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            time_attrs={"type": "time"},
        ),
        label="3차 결과 임시 발표일",
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
        fields = ["first_end_date", "second_end_date", "third_end_date"]


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ("title", "intro", "file", "content")
        labels = {
            "title": "제목",
            "intro": "한 줄 소개",
            "file": "첨부파일",
            "content": "내용",
        }
