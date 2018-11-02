from django.urls import path

from . import views

app_name = 'news_aggregator'

urlpatterns = [
    path('', views.NewsView.as_view(), name='news_list.html'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news_detail.html'),
    path('user/', views.UserView.as_view(), name='user_list.html'),
    path('tag/', views.TagView.as_view(), name='tag_list.html'),
    path('category/', views.CategoryView.as_view(), name='category_list.html'),
    path('resource/', views.ResourceView.as_view(), name='resource_list.html'),
]
