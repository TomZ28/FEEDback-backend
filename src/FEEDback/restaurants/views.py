from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.http import HttpResponse, HttpResponseBadRequest

from restaurants.models import Restaurant, RestaurantFollower, RestaurantLike, Comment
from restaurants.serializers import (SearchSerializer, CreateRestaurantSerializer, EditRestaurantSerializer,
RestaurantDetailSerializer, RestaurantFollowerSerializer, RestaurantLikeSerializer, CommentSerializer)
from restaurants.permissions import IsRestaurantOwner
from users.models import FEEDbackUser, Notification
from blogs.models import Blog
from blogs.serializers import BlogSerializer
from images.models import RestaurantImage
from images.serializers import RestaurantImageSerializer
from menuitems.models import MenuItem
from menuitems.serializers import MenuItemSerializer

# Create your views here.

class SearchView(ListAPIView):
    """
    Search for restaurants matching the given search fields.
    """
    permission_classes = (AllowAny,)
    search_fields = ['name', 'address', 'menuitems__name']
    filter_backends = (SearchFilter,)
    serializer_class = SearchSerializer
    queryset = Restaurant.objects.all().order_by('-follower_count')
    pagination_class = LimitOffsetPagination
    page_size = 20


class CreateRestaurantView(CreateAPIView):
    """
    Create a Restaurant. Requires that the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateRestaurantSerializer
    queryset = Restaurant.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EditRestaurantView(UpdateAPIView):
    """
    Edit the Restaurant with the given id, if it exists. Requires
    that the user is authenticated and owns the Restaurant.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = EditRestaurantSerializer
    queryset = Restaurant.objects.all()

    def get_object(self):
        # Check if current user owns restaurant
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        self.check_object_permissions(self.request, restaurant)
        return restaurant


class RestaurantDetailView(RetrieveAPIView):
    """
    Retrieve the details of the Blog with the given id, if it exists.
    """
    permission_classes = (AllowAny,)
    serializer_class = RestaurantDetailSerializer

    def get_object(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        return restaurant


class FollowRestaurantView(CreateAPIView):
    """
    Create a RestaurantFollower relationship between the user and the Restaurant
    with the given id. Increments the Restaurant's 'follower_count'. Requires that
    the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantFollowerSerializer

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])

        # Check if user already followed restaurant
        if RestaurantFollower.objects.filter(follower=self.request.user, restaurant=restaurant).exists():
            return HttpResponseBadRequest("User already followed restaurant")

        # Increment restaurant follower count
        restaurant.follower_count += 1
        restaurant.save()

        # Record that the user followed the restaurant
        serializer.save(restaurant=restaurant, follower=self.request.user)

        # Notify the restaurant owner
        msg = self.request.user.username + " followed your restaurant"
        notification = Notification(recipient=restaurant.owner, message=msg)
        notification.save()

class UnfollowRestaurantView(DestroyAPIView):
    """
    Delete the RestaurantFollower relationship between the user and the Restaurant
    with the given id, if it exists. Decrements the Restaurant's 'follower_count'.
    Requires that the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantDetailSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Restaurant.objects.filter(id=self.kwargs['id'])

    def perform_destroy(self, instance):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])

        # Check if user followed restaurant
        if not RestaurantFollower.objects.filter(follower=self.request.user, restaurant=restaurant).exists():
            return HttpResponseBadRequest("User did not previously follow restaurant")

        # Decrement restaurant follower count
        restaurant.follower_count -= 1
        restaurant.save()

        return super().perform_destroy(instance)


class LikeRestaurantView(CreateAPIView):
    """
    Create a RestaurantLike relationship between the user and the Restaurant
    with the given id. Increments the Restaurant's 'likes' count. Requires that
    the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantLikeSerializer

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])

        # Check if user already liked restaurant
        if RestaurantLike.objects.filter(liker=self.request.user, restaurant=restaurant).exists():
            return HttpResponseBadRequest("User already liked restaurant")

        # Increment restaurant like count
        restaurant.likes += 1
        restaurant.save()

        # Record that the user liked the restaurant
        serializer.save(restaurant=restaurant, liker=self.request.user)

        # Notify the restaurant owner
        msg = self.request.user.username + " liked your restaurant"
        notification = Notification(recipient=restaurant.owner, message=msg)
        notification.save()


class UnlikeRestaurantView(DestroyAPIView):
    """
    Delete the RestaurantLike relationship between the user and the Restaurant
    with the given id, if it exists. Decrements the Restaurant's 'likes' count.
    Requires that the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantDetailSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Restaurant.objects.filter(id=self.kwargs['id'])

    def perform_destroy(self, instance):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])

        # Check if user liked restaurant
        restaurant_likes = RestaurantLike.objects.filter(liker=self.request.user, restaurant=restaurant)
        if not restaurant_likes.exists():
            return HttpResponseBadRequest("User did not previously like restaurant")
        restaurant_like = restaurant_likes.first()
        restaurant_like.delete()

        # Decrement restaurant like count
        restaurant.likes -= 1
        restaurant.save()


class RestaurantImagesView(ListAPIView):
    """
    Retrieve a list of RestaurantImages belonging to the Restaurant with
    the given id.
    """
    permission_classes = (AllowAny,)
    serializer_class = RestaurantImageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        return RestaurantImage.objects.filter(restaurant=restaurant)

class AddImageView(CreateAPIView):
    """
    Create a RestaurantImage that belongs to the Restaurant with the given id.
    Requires that the user is authenticated and owns the Restaurant.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = RestaurantImageSerializer
    queryset = RestaurantImage.objects.all()

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        self.check_object_permissions(self.request, restaurant)
        serializer.save(restaurant=restaurant)


class RestaurantBlogsView(ListAPIView):
    """
    Retrieve a list of Blogs belonging to the Restaurant with the given id,
    with the most recent at the front.
    """
    serializer_class = BlogSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        blogs = Blog.objects.filter(restaurant=restaurant)
        return blogs.order_by('-date_created')


class AddBlogView(CreateAPIView):
    """
    Create a Blog that belongs to the Restaurant with the given id.
    Requires that the user is authenticated and owns the Restaurant.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        self.check_object_permissions(self.request, restaurant)
        serializer.save(restaurant=restaurant)

        # Notify all followers that a blog has been posted
        msg = restaurant.name + " posted a new blog"
        follower_ids = RestaurantFollower.objects.filter(restaurant=restaurant).exclude(follower_id__isnull=True).values_list('follower_id', flat=True)
        for follower_id in follower_ids:
            follower = FEEDbackUser.objects.get(id=follower_id)
            notification = Notification(recipient=follower, message=msg)
            notification.save()


class RestaurantCommentsView(ListAPIView):
    """
    Retrieve a list of Comments belonging to the Restaurant with the given id,
    with the most recent at the front.
    """
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        comments = Comment.objects.filter(restaurant=restaurant)
        return comments.order_by('-date_created')


class AddCommentView(CreateAPIView):
    """
    Create a Comment that belongs to the Restaurant with the given id.
    Requires that the user is authenticated and owns the Restaurant.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])

        # Increment restaurant rating count by 1
        restaurant.rating_count += 1
        restaurant.save()

        serializer.save(restaurant=restaurant, author=self.request.user)


class RestaurantMenuView(ListAPIView):
    """
    Retrieve a list of MenuItems belonging to the Restaurant with
    the given id.
    """
    serializer_class = MenuItemSerializer
    pagination_class = PageNumberPagination
    page_size = 10

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        menu_items = MenuItem.objects.filter(restaurant=restaurant)
        return menu_items


class AddMenuItemView(CreateAPIView):
    """
    Create a MenuItem that belongs to the Restaurant with the given id.
    Requires that the user is authenticated and owns the Restaurant.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        self.check_object_permissions(self.request, restaurant)
        serializer.save(restaurant=restaurant)

        # Notify all followers that a menu item has been added
        msg = restaurant.name + " added a new menu item"
        follower_ids = RestaurantFollower.objects.filter(restaurant=restaurant).exclude(follower_id__isnull=True).values_list('follower_id', flat=True)
        for follower_id in follower_ids:
            follower = FEEDbackUser.objects.get(id=follower_id)
            notification = Notification(recipient=follower, message=msg)
            notification.save()
