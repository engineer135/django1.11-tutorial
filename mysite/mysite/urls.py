# project 최상단의 urlconf(바로 지금 이 파일) 에서 polls.urls 모듈을 바라보도록 설정한다.
# app 은 특정한 기능을 수행하는 웹 어플리케이션이고, project 는 이런 특정 웹 사이트를 위한 app들과 각 설정들을 한데 묶어놓은 것.
# project는 다수의 app을 포함할 수 있고, app은 다수의 project에 포함될 수 있다.
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]