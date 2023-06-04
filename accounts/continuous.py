from .models import User
from writing.models import Post
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status

class ContinuousView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        today = datetime.now().date()
        if not Post.objects.filter(user_id = user.id,
                                created_at__year=today.year,
                                created_at__month=today.month,
                                created_at__day=today.day,).exists():
            user.continuous_cnt += 1
            user.save(update_fields=['continuous_cnt'])
        return Response(status=status.HTTP_200_OK)
    
class CronContinuousView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()

        today = datetime.now().date()
        prev_date = today - timedelta(days=1)
        posts = Post.objects.filter(
                                        created_at__year=prev_date.year,
                                        created_at__month=prev_date.month,
                                        created_at__day=prev_date.day
                                    )
        posts_user_id_set = set(posts.values_list('user_id', flat=True))
        for user in users:
            if user.id not in posts_user_id_set:
                user.continuous_cnt = 0
                user.save(update_fields=['continuous_cnt'])
        return Response(status=status.HTTP_200_OK)