from django.urls import path
from blogs.views import BlogDetailView, EditBlogView, DeleteBlogView, LikeBlogView, UnlikeBlogView

app_name='blogs'

urlpatterns = [
    path('<int:id>/details/', BlogDetailView.as_view(), name='blogDetails'),
    path('<int:id>/edit/', EditBlogView.as_view(), name='editBlog'),
    path('<int:id>/delete/', DeleteBlogView.as_view(), name='deleteBlog'),
    path('<int:id>/like/', LikeBlogView.as_view(), name='likeBlog'),
    path('<int:id>/unlike/', UnlikeBlogView.as_view(), name='unlikeBlog'),
]
