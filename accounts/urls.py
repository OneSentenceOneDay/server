from django.urls import path
from .views import *
from .email import *
app_name = 'accounts'


urlpatterns = [
    # 구글 소셜로그인
    path('submail/', SubMailView.as_view(), name='ContactView'),
    path('notice/', NoticeMailView.as_view(), name='NoviceView'),
    path('change-sub/', change_sub, name='change_sub'),
    path('make-nickname/', make_nickname, name='make_nickname'),
    path('google/login/', GetGoogleAccessView.as_view(), name='google_login'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_finish'),
    path('change-nickname/', change_nickname, name='nickname'),
]
