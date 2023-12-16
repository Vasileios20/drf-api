from django.urls import path
from .views import FollowerList, FollowerDetail

urlpatterns = [
    path('followers/', FollowerList.as_view(), name='follower_list'),
    path('followers/<int:pk>/', FollowerDetail.as_view(),
         name='follower_detail'),
]
