from django.urls import path
from .views import *
from .email import *
from .ranking import *
from .change import *
from .feedback import FeedbackListCreateView
from .continuous import *

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
    path('ranking/', LikeRankingVIew.as_view(), name='ranking'),
    path('feedback/', FeedbackListCreateView.as_view(), name='FeedbackListCreateView'),
    path('continuous/', ContinuousView.as_view(), name='ContinuousView'),
    path('croncontinuous/', CronContinuousView.as_view(), name='CronContinuousView'),
    path('rankingcontinuous/', ContinuousRankingView.as_view(), name='ContinuousRankingView'),
]
