import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question

# 테스트시 이렇게 test.py 파일을 만들고
# 터미널에서 $ python manage.py test polls 커맨드로 실행한다.
# 테스트 시스템은 test로 시작하는 파일에서 테스트를 자동으로 찾아서(메소드 이름이 test로 시작하는 것들) 수행한다!
class QuestionModelTests(TestCase):
    # 미래 시간으로 포스팅된 퀘스쳔이 어제 안에 게신된 경우 true를 반환하는 함수에서도 true를 반환하는 버그를 테스트해보자(false가 나와야 맞음! 미래니까!)
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False) # false가 되어야 함. 하지만 결과는? true! 따라서 해당 함수의 수정이 필요한 것임을 알수있음!

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

