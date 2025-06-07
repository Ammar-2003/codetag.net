from django.urls import path , include
from .views import (
    PostListView,
    PostDetailView,
    CategoryPostListView,
    SearchPostsView
)
    

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name='category_posts'),
    path('search/', SearchPostsView.as_view(), name='search_posts')
]
