from django import forms
from post.models import Question, Answer



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'target', 
            'desired_language', 
            'preferred_day', 
            'preferred_time', 
            'online_offline', 
            'location', 
            'contact_method', 
            'subject', 
            'content',
            'calendar_link',
            'contact_info'
        ]
        
        labels = {
            'target': '목표 설정',
            'desired_language': '희망 언어',
            'preferred_day': '희망 요일',
            'preferred_time': '희망 시간',
            'online_offline': '온/오프라인',
            'location': '희망 장소',
            'contact_method': '연락 수단',
            'subject': '제목',
            'content': '내용',
            'calendar_link': '캘린더 링크',
            'contact_info': '연락 정보',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }