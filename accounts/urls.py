from django.urls import path
from .views import *
app_name = 'accounts'


urlpatterns = [
    # 구글 소셜로그인
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
     path('sendemail/', ContactView.as_view(), name='ContactView'),
]
