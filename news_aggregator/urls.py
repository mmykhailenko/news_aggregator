from django.urls import path

from . import views

app_name = 'news_aggregator'

urlpatterns = [
    path('', views.NewsView.as_view()),
    path('user/', views.UserView.as_view()),
    path('tag/', views.TagView.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('resource/', views.ResourceView.as_view()),
]
