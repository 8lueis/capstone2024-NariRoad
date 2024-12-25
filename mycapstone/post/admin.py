from django.contrib import admin
from .models import Question

# 제목(subject)으로 질문 데이터를 검색
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)
