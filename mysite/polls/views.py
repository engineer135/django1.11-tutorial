from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Question, Choice

# Create your views here.
# 기존 index, detail, results를 제네릭 뷰로 교체
# 자바 제네릭처럼.. 페이지의 형태를 명시해주는 거라고 보면 될것 같다.
# ListView, DetailView 상속만 해주면, 자동으로 매핑까지 알아서 해주고 편하긴 하네
# 제너릭 뷰 사용시 템플릿 디폴트는 <app name>/<model name>_list.html, <app name>/<model name>_detail.html 이런식인데 아래처럼 명시해서 쓸 수 있다.
# 컨텍스트 변수도 디폴트는 question_list지만 context_object_name을 명시적으로 써주면 그걸로 대체된다.
# 복잡한 화면에서는 힘들수도 있겠는데...?
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # choice_set 있는 애들만 보여준다.
        return Question.objects.annotate(choice_count=Count('choice')).filter(
            # 미래 날짜의 게시글을 가져오기 않기 위해 필터 추가
            pub_date__lte = timezone.now(),
            choice_count__gt = 0
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    # 미래의 포스트는 나오지 않도록 함수를 추가해준다.
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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