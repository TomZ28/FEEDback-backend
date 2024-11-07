from django.urls import path
from images.views import DeleteImageView

app_name='images'

urlpatterns = [
    path('<int:id>/delete/', DeleteImageView.as_view(), name='deleteImage'),
]
