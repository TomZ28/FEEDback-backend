from django.urls import path
from menuitems.views import EditMenuItemView, DeleteMenuItemView

app_name='menuitems'

urlpatterns = [
    path('<int:id>/edit/', EditMenuItemView.as_view(), name='editImage'),
    path('<int:id>/delete/', DeleteMenuItemView.as_view(), name='deleteImage'),
]
