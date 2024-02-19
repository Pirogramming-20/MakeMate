from django import forms
from apps.group.models import Idea

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