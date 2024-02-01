from django import forms
from .models import Group
from .models import Idea 


class GroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields = ('__all__')
        labels = {
            
        }

class IdeaForm(forms.ModelForm):
    class Meta():
        model = Idea
        fields = ('__all__')
        labels = {
            'idea_title': '제목', 
            'idea_intro': '한 줄 소개',
            'idea_file': '첨부파일', 
            'idea_content': '내용',
        }
            