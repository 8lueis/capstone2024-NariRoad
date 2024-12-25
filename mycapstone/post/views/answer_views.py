from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from ..models import Question, Answer
from ..forms import AnswerForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('post:detail', question_id = question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'post/question_detail.html', context)



@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('post:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('post:detail', question_id = answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'post/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('{}#answer_{}'.format(
                resolve_url('post:detail', question_id = answer.question.id), answer.id))
            

def send_calendar_info(request, question_id, answer_id):
    """
    질문의 작성자가 댓글 작성자에게 캘린더 링크와 연락 정보를 전송하는 함수
    """
    # 질문 객체와 댓글 객체 가져오기
    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(Answer, id=answer_id)
    
    sender_email = question.author.email  # 발신자: 질문 작성자의 이메일
    recipient_email = answer.author.email  # 수신자: 댓글 작성자의 이메일
    
    # 캘린더 링크와 연락 정보가 있는지 확인
    if question.contact_method and question.calendar_link:
        try:
            send_mail(
                '스터디 초대 정보 (나리로드 전송)',  # 이메일 제목
                f"안녕하세요, {answer.author.username}님!\n\n스터디 초대 정보입니다.\n\n캘린더 링크: {question.calendar_link}\n연락 정보: {question.contact_method}\n\n문의 사항이 있으면 발신자에게 회신해 주세요.",  # 이메일 내용
                sender_email,  # 발신자 이메일 (글 작성자)
                [recipient_email],  # 수신자 이메일 (댓글 작성자)
            )
            return JsonResponse({'message': '초대 정보가 이메일로 전송되었습니다.'})
        except Exception as e:
            return JsonResponse({'error': f'이메일 전송에 실패했습니다: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': '정보가 입력되지 않았습니다.'}, status=400)