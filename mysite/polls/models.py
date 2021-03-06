import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model) :
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) :
        return self.question_text
    
    def was_published_recently(self) :
        # 어제 오늘 사이의 Question만 True 리턴(맞나?)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # 관리자 페이지에서 보여줄 명칭 및 순서 수정 가능
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model) :
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) :
        return self.choice_text
