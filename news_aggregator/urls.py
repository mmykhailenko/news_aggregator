from django.urls import path
from news_aggregator import views

app_name = 'news_aggregator'
urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_single'),
    path('news/<str:category_name>', views.NewsByCategoryListView.as_view(), name='news_category_list'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('resource/', views.ResourceListView.as_view(), name='resource_list'),
    path('docs/', views.documentation_view, name='docs'),
]
