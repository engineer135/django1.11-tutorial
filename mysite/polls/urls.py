from django.urls import path
from . import views

urlpatterns = [
    # ex : /polls/
    path('', views.index, name='index'),
    # ex : /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex : /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex : /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

# url 함수에 넘겨야하는 인수
# regex(필수) 정규표현식. 너무 복잡하게 쓰지는 말자. 느려진다.
# view(필수)
# kwargs(선택) 파라미터인듯? 딕셔너리 형태
# name(선택) URL 에 이름을 지으면, 템플릿을 포함한 Django 어디에서나 명확하게 참조할 수 있습니다. 
# 이 강력한 기능을 이용하여, 단 하나의 파일만 수정해도 project 내의 모든 URL 패턴을 바꿀 수 있도록 도와줍니다.