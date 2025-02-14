from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
