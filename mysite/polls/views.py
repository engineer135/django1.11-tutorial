from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from .models import Question

# Create your views here.
def index(request) :
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 하드코딩 대신 템플릿 사용하자
    context = {
        'latest_question_list' : latest_question_list,
    }
    # render 함수 인수는 request, template이름, context 객체를 넘겨주면 된다!
    return render(request, 'polls/index.html', context)

def detail(request, question_id) :
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist :
    #     raise Http404('Question 없음!')

    # 지름길 사용하자 get_object_or_404()
    # 리스트인 경우엔 get_list_or_404()를 쓰면 된다.
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id) :
    response = "너는 질문의 결과를 보고 있어 %s"
    return HttpResponse(response % question_id)

def vote(request, question_id) :
    return HttpResponse("너는 지금 %s에 투표중이야" % question_id)