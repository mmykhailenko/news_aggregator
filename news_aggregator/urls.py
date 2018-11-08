from django.urls import path, include
from news_aggregator import views

app_name = 'news_aggregator'
urlpatterns = [
    path('news/', include([
        path('', views.NewsListView.as_view(), name='news_list'),
        path('<int:pk>/', views.NewsDetailView.as_view(), name='news_single'),
        path('category=<str:category_name>',
             views.NewsByCategoryListView.as_view(),
             name='news_category_list'),
    ])),
    path('resource/', views.ResourceListView.as_view(), name='resource_list'),
    path('docs/', views.documentation_view, name='docs'),
]
