from django.urls import path
from django.views import generic
from news_aggregator import views

app_name = 'news_aggregator'
urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_single'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('resource/', views.ResourceListView.as_view(), name='resource_list'),
    path('worker/', views.NewsCreator.as_view(), name='news_creator'),
]
