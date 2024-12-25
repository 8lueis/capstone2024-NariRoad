from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


# 로그아웃 상태이면 AnonymousUser 객체가, 로그인 상태이면 User 객체가 들어있음  
# => @login_required(login_url='common:login')추가해서 로그아웃 상태에서 자동으로 로그인 화면으로....

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        # 수정하려는 질문과 글쓴이가 다를 경우 수정 권한 Xx
        messages.error(request, '수정 권한이 없습니다.') # 넌-필드 오류 발생시킴 
        return redirect('post:detail', question_id=question.id)
        # 수정 버튼 클릭하면 GET 방식으로 호출되어 질문 수정 화면이 보여짐 
    if request.method == "POST":
        # 저장하기 클릭 시 POST 방식으로 호출되어 수정됨 
        form = QuestionForm(request.POST, instance=question)
        # POST 요청인 경우 수정된 내용 반영을 위해 폼 작성 (request.POST의 값으로 덮어써라)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('post:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
        # GET 요청인 경우 제목과 내용이 반영될 수 있도록 폼 생성 
    context = {'form': form}
    return render(request, 'post/question_form.html',context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('post:detail', question_id=question.id)
    question.delete()
    return redirect('post:index')


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # 폼이 유효하다면 
            question = form.save(commit=False) # 임시 저장 후 question 객체 리턴 받음 
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now() # 실제 저장을 위한 작성 일시 설정 
            question.save() # 실제로 데이터 저장 
            return redirect('post:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'post/question_form.html', context)

