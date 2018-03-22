from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id) :
    question = get_object_or_404(Question, pk=question_id)
    print(question)
    try :
        # 명시적으로 post데이터만 쓰려고 request.POST[] 사용
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist) :
        print('except!!')
        # post 자료에 choice 가 없는 경우 keyError 발생
        # 투표 폼을 다시 보여준다
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "초이스한 항목이 없어!",
        })
    else :
        selected_choice.votes += 1
        selected_choice.save()
        # 리다이렉트로 리턴. 중복 서브밋 방지
        # reverse 함수는 url을 하드코딩하지 않도록 도와준다.
        # 이때 args는 itrable해야하므로, 마지막에 콤마를 꼭 써줘야한다. 안그러면 에러남.
        # 아래 reverse 함수는 '/polls/3/results/' 같은 문자열을 반환한다.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))