from django.contrib import admin
from .models import Question, Choice

# Register your models here.
class ChoiceInline(admin.TabularInline): #StackedInline 상속받는 경우 밑으로 길게 생김. TabularInline는 좀 더 컴팩트한 사이즈.
    model =  Choice
    extra = 3

# 관리자 폼 커스터마이징(fields 배열 순서대로 보여줍니다)
class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    # 항목이 많은 경우 fieldsets 로 관리합니다. 각 튜플의 첫번째 요소는 fieldset의 제목.
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date information', {'fields':['pub_date']}),
    ]
    
    # Choice 객체는 Question 관리자 페이지에서 편집됩니다. 기본으로 3가지 선택항목 제공! 이라고 장고에 알려주는 격이다.
    # inlines를 추가하면, 관리자페이지 Question 상세보기 들어가면 자동으로 3가지 Choice 등록할 수 있도록 화면 생성해준다.
    inlines=[ChoiceInline]

    # 리스트 레이아웃 설정. 기본값은 그냥 __str__ 값
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # 리스트 필터 추가도 가능하다
    list_filter = ['pub_date']

    # 검색 기능도 마찬가지. like검색이 default.. 변경되는지는 모르겠넹..
    search_fields = ['question_text']

    # 이외에도 기본 페이징 제공(100개)

# 관리 사이트에서 poll app 변경가능하도록 추가
admin.site.register(Question, QuestionAdmin)

# choice도 관리자에 나타난다. 이 경우 자동으로 설문항목 폼에서 Question 등록이 가능하다. 그런데 이렇게 하면 불편하므로 쓰지 않는다. 
# 대신 question 폼 페이지에서 choice를 등록할 수 있게 커스터마이징하자.
#admin.site.register(Choice) 
