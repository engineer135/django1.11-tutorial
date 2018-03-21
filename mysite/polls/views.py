from django.http import HttpResponse

# Create your views here.
def index(request) :
    return HttpResponse("Hello~~~ You're at the polls index.")

def detail(request, question_id) :
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id) :
    response = "너는 질문의 결과를 보고 있어 %s"
    return HttpResponse(response % question_id)

def vote(request, question_id) :
    return HttpResponse("너는 지금 %s에 투표중이야" % question_id)