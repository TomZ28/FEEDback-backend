from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from restaurants.views import (CreateRestaurantView, EditRestaurantView, RestaurantDetailView, 
FollowRestaurantView,  SearchView, UnfollowRestaurantView, LikeRestaurantView, 
UnlikeRestaurantView, RestaurantImagesView, AddImageView, RestaurantBlogsView, 
AddBlogView, RestaurantCommentsView, AddCommentView, RestaurantMenuView, AddMenuItemView)

app_name='restaurants'

urlpatterns = [
    path('search/', SearchView.as_view(), name='restaurantSearch'),
    path('create/', CreateRestaurantView.as_view(), name='createRestaurant'),
    path('<int:id>/details/', RestaurantDetailView.as_view(), name='restaurantDetails'),
    path('<int:id>/edit/', EditRestaurantView.as_view(), name='editRestaurant'),
    path('<int:id>/images/', RestaurantImagesView.as_view(), name='restaurantImages'),
    path('<int:id>/images/add/', AddImageView.as_view(), name='addImage'),
    path('<int:id>/blogs/', RestaurantBlogsView.as_view(), name='restaurantBlogs'),
    path('<int:id>/blogs/add/', AddBlogView.as_view(), name='addBlog'),
    path('<int:id>/comments/', RestaurantCommentsView.as_view(), name='restaurantComments'),
    path('<int:id>/comments/add/', AddCommentView.as_view(), name='addComment'),
    path('<int:id>/menu/', RestaurantMenuView.as_view(), name='restaurantMenu'),
    path('<int:id>/menu/add/', AddMenuItemView.as_view(), name='addMenuItem'),
    path('<int:id>/like/', LikeRestaurantView.as_view(), name='likeRestaurant'),
    path('<int:id>/unlike/', UnlikeRestaurantView.as_view(), name='unlikeRestaurant'),
    path('<int:id>/follow/', FollowRestaurantView.as_view(), name='followRestaurant'),
    path('<int:id>/unfollow/', UnfollowRestaurantView.as_view(), name='unfollowRestaurant'),
]
