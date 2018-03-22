import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

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

def create_question(question_text, days, choice_create=True):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    if choice_create :
        question.choice_set.create(choice_text='default choice', votes=0)
    
    return question

# shell에서 진행하는 경우
# >>> from django.test.utils import setup_test_environment
# >>> setup_test_environment()
# response.context와 같은 response의 추가적인 속성을 사용할수 있게 하기위해서 setup_test_environment()를 사용하여 템플릿 렌더러를 설치합니다. 
# 이 메소드는 테스트 데이터베이스를 셋업하지 않습니다. 그렇기때문에 테스트는 현재 사용중인 데이터베이스위에서 돌게되며 
# 결과는 데이터베이스에 이미 만들어져있는 질문들에 따라서 조금씩 달라질수 있습니다.

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
    
    def test_no_choice_set_questions(self):
        # 선택 사항이 없는 설문은 인덱스에 나오지 않도록 처리
        create_question(question_text='no choice question', days=-3, choice_create=False)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
