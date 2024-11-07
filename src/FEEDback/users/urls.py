from django.urls import path

from users.views import SignupView, EditProfileView, FeedView, NotificationView, FEEDbackTokenObtainPairView

app_name='users'

urlpatterns = [
    path('login/', FEEDbackTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/edit/', EditProfileView.as_view(), name='editProfile'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('notifications/', NotificationView.as_view(), name='notifications')
    #path('logout/', logout, name='logout'), Logout not required for P2
]
