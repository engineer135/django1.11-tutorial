from django.http import HttpResponse
from django.template import loader
from .models import Question

# Create your views here.
def index(request) :
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 하드코딩 대신 템플릿 사용하자
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list' : latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id) :
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id) :
    response = "너는 질문의 결과를 보고 있어 %s"
    return HttpResponse(response % question_id)

def vote(request, question_id) :
    return HttpResponse("너는 지금 %s에 투표중이야" % question_id)