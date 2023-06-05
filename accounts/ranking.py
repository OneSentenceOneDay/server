from django.utils import timezone
from django.db.models import Count
from rest_framework import generics
from .models import User
from writing.models import Post
from .serializers import UserDetailSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime, timedelta

class LikeRankingVIew(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        top_users = Post.objects.filter(created_at__range=[start_of_week.date(), end_of_week.date()])\
            .values('user')\
            .annotate(total_likes=Count('like_users'))\
            .order_by('-total_likes')\
            .values('total_likes','user__nickname')

        return Response({'ranking': list(top_users)}, status=status.HTTP_200_OK)

class ContinuousRankingView(APIView):
    def get(self, request, *args, **kwargs):
        top_users = User.objects.order_by('-continuous_cnt')[:3].values_list('nickname', flat=True)
        return Response({'ranking': top_users}, status=status.HTTP_200_OK)
    




