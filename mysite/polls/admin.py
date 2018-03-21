from django.contrib import admin
from .models import Question

# Register your models here.
# 관리 사이트에서 poll app 변경가능하도록 추가
admin.site.register(Question)
