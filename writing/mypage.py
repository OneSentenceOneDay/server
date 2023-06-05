
from rest_framework.response import Response
from writing.models import Post
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class MypageTodayIWroteView(ListAPIView):
    serializer_class = MypageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    #pagination_class = SentencePagination

    def get_queryset(self):
        user_id = self.request.user.id
        today = datetime.now().date()
        return Post.objects.filter(user_id=user_id,
                                   created_at__year=today.year,
                                   created_at__month=today.month,
                                   created_at__day=today.day,).order_by('-created_at')
    
@api_view(['GET'])
def get_dates(request):
    dateDict = {0: '월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}
    dates = {}
    today = datetime.now().date()
    #dates['today'] = today.strftime('%y.%m.%d') + ' ' + dateDict[today.weekday()]
    for i in range(1, 8):
        date = today - timedelta(days=i)
        try: 
            sentence = Sentence.objects.get(
                                   created_at__year=date.year,
                                   created_at__month=date.month,
                                   created_at__day=date.day,).sentence
        except:
            sentence = None
        dates['today_sentence'] = Sentence.objects.get(
                        created_at__year=today.year,
                        created_at__month=today.month,
                        created_at__day=today.day,).sentence
        dates[f'{i}_days_ago'] = {
                "summary": date.strftime('%m/%d'),
                "detail": date.strftime('%Y.%m.%d') + ' ' + dateDict[date.weekday()],
                "sentence": sentence
            }
    return Response(dates)

class MypageOrderView(ListAPIView):
    serializer_class = MypageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    #pagination_class = MypagePagination

    def get_queryset(self):
        date = self.kwargs.get("date")
        month, day = date.split("&")
        user_id = self.request.user.id
        return Post.objects.filter(created_at__year='2023',
                                   created_at__month=month,
                                   created_at__day=day,
                                   user_id=user_id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class MypageUserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        posts = Post.objects.filter(user_id = user.id)
        post_num = posts.count()
        continuous_cnt = user.continuous_cnt
       
        upper_users = list(User.objects.filter(continuous_cnt__gt=user.continuous_cnt).values_list('id'))
        continuous_ranking = len(upper_users) + 1
        data = {
            "post_num" : post_num,
            "continuous_cnt": continuous_cnt,
            "liked_num": user.liked_num,
            "continuous_ranking": continuous_ranking
        }
        return Response(data)

class WhatILikeView(ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.like.all().order_by('-created_at')
    

# class WeekIsWritingView(APIView):
#     def get(self, *args, **kwargs):
#         today = datetime.today()
#         start_of_week = today - timedelta(days=today.weekday())
#         end_of_week = start_of_week + timedelta(days=6)
#         user = self.request.user
#         result = {str((start_of_week + timedelta(days=i)).date()): 0 for i in range(7)}
        
#         post_dates = Post.objects.filter(user_id=user.id, created_at__range=[start_of_week.date(), end_of_week.date() + timedelta(days=1)]).only('created_at')
        
#         if post_dates.exists():
#             for post in post_dates:
#                 date = str(post.created_at.date())
#                 result[date] = 1
#         else:
#             return Response({'week_is_writing': result}, status=status.HTTP_200_OK)
#         return Response({'week_is_writing': result}, status=status.HTTP_200_OK)
# class WeekIsWritingView(APIView):
#     def get(self, *args, **kwargs):
#         today = datetime.today()
#         start_of_week = today - timedelta(days=today.weekday())
#         end_of_week = start_of_week + timedelta(days=6)
#         user = self.request.user
#         result = [0] * 7
        
#         post_dates = Post.objects.filter(user_id=user.id, created_at__range=[start_of_week.date(), end_of_week.date()]).only('created_at')
#         if post_dates.exists():
#             for post in post_dates:
#                 date = (post.created_at.date() - start_of_week.date()).days
#                 result[date] = 1
#         else:
#             return Response({'week_is_writing': result}, status=status.HTTP_200_OK)
        
#         return Response({'week_is_writing': result}, status=status.HTTP_200_OK)
  

class WeekIsWritingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        user = self.request.user
        result = {str((start_of_week + timedelta(days=i)).date()): 0 for i in range(7)}
        
        post_dates = Post.objects.filter(user_id=user.id, created_at__range=[start_of_week.date(), end_of_week.date()]).only('created_at')
        if post_dates.exists():
            for post in post_dates:
                date = str(post.created_at.date())
                result[date] = 1
        
        return Response({'week_is_writing': list(result.values())}, status=status.HTTP_200_OK)