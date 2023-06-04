from .models import User
from writing.models import Post
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status

class ContinuousView(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        today = datetime.now().date()
        prev_date = today - timedelta(days=1)
        if not Post.objects.filter(user_id = user.id,
                                created_at__year=prev_date.year,
                                created_at__month=prev_date.month,
                                created_at__day=prev_date.day,).exists():
            user.continuous_cnt = 0
            user.save(update_fields=['continuous_cnt'])
        return Response(status=status.HTTP_200_OK)
        
        
    def post(self, request, *args, **kwargs):
        user = self.request.user
        today = datetime.now().date()
        if not Post.objects.filter(user_id = user.id,
                                created_at__year=today.year,
                                created_at__month=today.month,
                                created_at__day=today.day,).exists():
            print("yes")
            user.continuous_cnt += 1
            user.save(update_fields=['continuous_cnt'])
        return Response(status=status.HTTP_200_OK)