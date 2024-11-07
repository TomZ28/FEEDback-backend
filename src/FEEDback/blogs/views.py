from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponse, HttpResponseBadRequest

from blogs.models import Blog, BlogLike
from blogs.serializers import BlogSerializer, BlogLikeSerializer
from restaurants.models import Restaurant
from restaurants.permissions import IsRestaurantOwner
from users.models import Notification

# Create your views here.

class EditBlogView(UpdateAPIView):
    """
    Edit the Blog with the given id. Requires that the user is authenticated and
    owns the restaurant that posted the blog.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        blog = get_object_or_404(queryset, id=self.kwargs['id'])

        # Check if current user owns restaurant
        self.check_object_permissions(self.request, blog.restaurant)

        return blog


class DeleteBlogView(DestroyAPIView):
    """
    Delete the Blog with the given id, if it exists. Requires that the user is
    authenticated and owns the restaurant that posted the blog.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = 'id'

    def perform_destroy(self, instance):
        queryset = self.get_queryset()
        blog = get_object_or_404(queryset, id=self.kwargs['id'])

        # Check if current user owns restaurant
        self.check_object_permissions(self.request, blog.restaurant)

        return super().perform_destroy(instance)


class BlogDetailView(RetrieveAPIView):
    """
    Retrieve the details of the Blog with the given id, if it exists.
    """
    serializer_class = BlogSerializer

    def get_object(self):
        return get_object_or_404(Blog, id=self.kwargs['id'])


class LikeBlogView(CreateAPIView):
    """
    Create a BlogLike relationship between the user and the Blog with the given id.
    Increments the Blog's 'likes' count. Requires that the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogLikeSerializer

    def perform_create(self, serializer):
        blog = get_object_or_404(Blog, id=self.kwargs['id'])
        # Check if user already liked blog
        if BlogLike.objects.filter(liker=self.request.user, blog=blog).exists():
            return HttpResponseBadRequest("User already liked post")

        # Increment blog like count
        blog.likes += 1
        blog.save()

        # Record that the user liked the blog
        serializer.save(blog=blog, liker=self.request.user)

        # Notify the restaurant owner
        msg = self.request.user.username + " liked your blog post"
        notification = Notification(recipient=blog.restaurant.owner, message=msg)
        notification.save()


class UnlikeBlogView(DestroyAPIView):
    """
    Delete the BlogLike relationship between the user and the Blog with the given id,
    if it exists. Becrements the blog's 'likes' count. Requires that the user is
    authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Blog.objects.filter(id=self.kwargs['id'])

    def perform_destroy(self, instance):
        blog = get_object_or_404(Blog, id=self.kwargs['id'])

        # Check if user liked blog
        blog_likes = BlogLike.objects.filter(liker=self.request.user, blog=blog)
        if not blog_likes.exists():
            return HttpResponseBadRequest("User did not previously like blog")
        blog_like = blog_likes.first()
        blog_like.delete()

        # Decrement blog like count
        blog.likes -= 1
        blog.save()