from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question


def index(request):
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어 
    question_list = Question.objects.order_by('-create_date')  # 최신순으로 정렬 
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    # -: 작성일시 역순으로 정렬(order_by)하라는 의미
    paginator = Paginator(question_list, 10) # 페이지당 10개 
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page':page, 'kw':kw}
    question_list = Question.objects.order_by('-create_date')
    return render(request, 'post/question_list.html', context)

def detail(request, question_id):
    question =get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'post/question_detail.html', context)

