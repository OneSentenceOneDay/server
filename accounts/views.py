from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_framework import status
from email.message import EmailMessage
from django.core.mail import send_mail
from .models import *
from writing.models import Subsription, Sentence
from .serializers import *
from dj_rest_auth.registration.views import SocialLoginView, LoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from django.shortcuts import redirect
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.decorators import api_view, authentication_classes
from json import JSONDecodeError
from django.http import JsonResponse
import requests
from rest_framework import generics, status
from .models import *
from allauth.socialaccount.models import SocialAccount 
from rest_framework_simplejwt.authentication import JWTAuthentication
from pathlib import Path
import os, json 
from django.core.exceptions import ImproperlyConfigured 
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework.exceptions import MethodNotAllowed
from django.http import HttpResponseRedirect
User = get_user_model()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json')
with open(secret_file, 'r') as f: #open as로 secret.json을 열어줍니다.
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets): #예외 처리를 통해 오류 발생을 검출합니다.
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

#################################
def get_day_of_the_week(input_created_at):
    dateDict = {0: '월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}
    created_at = input_created_at
    day_of_the_week = dateDict[created_at.weekday()]
    return day_of_the_week

#################################
class CustomLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()
    
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )
            access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)
            auth_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', False)

            data = {
                'user': self.user,
                'access_token': self.access_token,
            }

            if not auth_httponly:
                data['refresh_token'] = self.refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data['refresh_token'] = ""

            if return_expiration_times:
                data['access_token_expiration'] = access_token_expiration
                data['refresh_token_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        if self.user.is_first:
            self.user.is_first = False
            self.user.save(update_fields=['is_first'])
    
        if getattr(settings, 'REST_USE_JWT', False):
            from dj_rest_auth.jwt_auth import set_jwt_cookies
            set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response


class ReceiveConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect(redirect_to='http://localhost:3000')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect(redirect_to='http://localhost:3000')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs
    
class CustomConfirmEmailView(ConfirmEmailView):
    pass

class CustomVerifyEmailView(APIView, CustomConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': ('ok')}, status=status.HTTP_200_OK)

#################################################
####################구글##########################
#################################################
BASE_URL = 'https://port-0-osod-108dypx2ale9l8kjq.sel3.cloudtype.app/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/login/'

state = "vyv2dj"

class GetGoogleAccessView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        email_req_status = email_req.status_code
        
        if email_req_status != 200:
            return Response({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
        email_req_json = email_req.json()
        email = email_req_json.get('email')

        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)
            
            if social_user.provider != 'google':
                return Response({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.is_first:
                user.is_first = False
                user.save(update_fields=['is_first'])

            data = {'access_token': access_token}
            accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
            accept_status = accept.status_code
            
            if accept_status != 200:
                return Response({'err_msg': 'failed to signin'}, status=accept_status)

            accept_json = accept.json()
            return Response(accept_json)
        
        except User.DoesNotExist:
            data = {'access_token': access_token}
            
            accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
            
            accept_status = accept.status_code

            if accept_status != 200:
                return Response({'err_msg': 'failed to signup'}, status=accept_status)
            accept_json = accept.json()
            
            return Response(accept_json)

        except SocialAccount.DoesNotExist:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)     

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    permission_classes = [AllowAny]


class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["uid"] = self.kwargs.get("uid")
        data["token"] = self.kwargs.get("token")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': ('Password has been reset with the new password.')},
        )

class ContactView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sub_users = User.objects.filter(subscription=True)
        sub_unknowns = Subsription.objects.all()

        today = datetime.now().date()
        target_sentence = Sentence.objects.get(
                                created_at__year=today.year,
                                created_at__month=today.month,
                                created_at__day=today.day,
                                )

        sub_users_list = [sub_user.email for sub_user in sub_users]
        sub_unknowns_list = [sub_unknown.sub_email for sub_unknown in sub_unknowns]
        send_list = sub_users_list + sub_unknowns_list
        send_list = set(send_list)
        send_list = list(send_list)

        context = {
            'created_at': target_sentence.created_at,
            "day_of_the_week": get_day_of_the_week(target_sentence.created_at),
            'sentence': target_sentence.sentence,
            'discription': target_sentence.discription,
            'translate': target_sentence.translate,
        }

        message = render_to_string('email_template.html', context)
        subject = f"[OSOD] {get_day_of_the_week(target_sentence.created_at)}의 영작"
        to = send_list
        send_mail(
            subject = subject,
            message = "",
            from_email = None,
            recipient_list = to,
            html_message = message
        )
        return Response(status.HTTP_201_CREATED)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def change_sub(request):
    user = request.user
    target = User.objects.get(id=user.id)
    if target.subscription:
        target.subscription = False
    else:
        target.subscription = True
    target.save(update_fields=['subscription'])

    return Response({
        "subscription": user.subscription,
    },status = status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def make_nickname(request):
    try:
        user = request.user
        get_nick = request.data.get('nickname')
        #get_name = request.data.get('name')
        if user.first_name:
            user.name = user.last_name + user.first_name
        user.nickname = get_nick
        user.save(update_fields=['nickname', 'name'])
        return Response({
            "nickname": user.nickname,
            'name': user.name
        },status = status.HTTP_200_OK)
    except:
        return Response({
            "detail": "중복이거나 형식이 잘못됐습니다.",
        },status = status.HTTP_400_BAD_REQUEST)