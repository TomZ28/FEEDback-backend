from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import FEEDbackUser, Notification
from restaurants.models import RestaurantFollower
from blogs.models import Blog

from users.serializers import NotificationSerializer, SignupSerializer, EditProfileSerializer, FEEDbackTokenObtainPairSerializer
from blogs.serializers import BlogSerializer

# Create your views here.

class SignupView(CreateAPIView):
    """
    Signs the user up to FEEDback.
    """
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    queryset = FEEDbackUser.objects.all()


class EditProfileView(RetrieveUpdateAPIView):
    """
    Edit the user's profile. Requires that the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EditProfileSerializer
    queryset = FEEDbackUser.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class FeedView(ListAPIView):
    """
    Retrieve a list of Blogs that were sent to the user, with the most
    recent at the front. Requires that the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        restaurant_ids = RestaurantFollower.objects.filter(follower=self.request.user).values_list('restaurant', flat=True)
        blogs = Blog.objects.filter(restaurant_id__in=restaurant_ids)
        return blogs.order_by('-date_created')


class NotificationView(ListAPIView):
    """
    Retrieve a list of Notifications that were sent to the user, with
    the most recent at the front. Requires that the user is authenticated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination
    page_size = 5

    def get_queryset(self):
        notifications = Notification.objects.filter(recipient=self.request.user)
        return notifications.order_by('-when')

class FEEDbackTokenObtainPairView(TokenObtainPairView):
    serializer_class = FEEDbackTokenObtainPairSerializer