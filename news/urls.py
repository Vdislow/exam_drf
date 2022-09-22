from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# router = DefaultRouter()
# router.register('news', views.NewsListCreateView, basename='news')

urlpatterns = [
    path('news/', views.NewsListCreateView.as_view(), name='news-create-list'),
    path('news/<int:pk>', views.NewsRetrieveUpdateDestroyView.as_view(), name='news_rud'),
    path('news/<int:news_id>/comments', views.CommentListCreateView.as_view(), name='comment_create_list'),
    path('news/<int:news_id>/comments/<int:pk>', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment_rud'),
    path('statuses', views.StatusesListCreate.as_view(), name='status_create_list'),
    path('statuses/<int:pk>', views.StatusesRetrieveUpdateDestroyView.as_view(), name='status_rud'),
    path('news/<int:news_id>/<str:status_slug>', views.NewsStatusGET.as_view(), name='status_news_add'),
    path('news/<int:news_id>/comments/<int:comment_id>/<str:status_slug>', views.CommentStatusGET.as_view(), name='status_comment_add'),
]
