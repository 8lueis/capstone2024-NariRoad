from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    # UserCreationForm 클래스를 상속 == 이메일 등의 속성을 추가하기 위함 
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
        # password1, 2 대조하기 위한 값 