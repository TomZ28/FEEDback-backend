from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from menuitems.models import MenuItem
from menuitems.serializers import MenuItemSerializer
from restaurants.permissions import IsRestaurantOwner

# Create your views here.

class EditMenuItemView(UpdateAPIView):
    """
    Edit the MenuItem with the given id, if it exists. Requires that the user is
    authenticated and owns the restaurant that added the MenuItem.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

    def get_object(self):
        menuItem = get_object_or_404(MenuItem, id=self.kwargs['id'])

        # Check if current user owns restaurant
        self.check_object_permissions(self.request, menuItem.restaurant)

        return menuItem


class DeleteMenuItemView(DestroyAPIView):
    """
    Delete the MenuItem with the given id, if it exists. Requires that the user is
    authenticated and owns the restaurant that added the MenuItem.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = MenuItemSerializer
    lookup_field = 'id'
    queryset = MenuItem.objects.all()

    def perform_destroy(self, instance):
        menuItem = get_object_or_404(MenuItem, id=self.kwargs['id'])

        # Check if current user owns restaurant
        self.check_object_permissions(self.request, menuItem.restaurant)

        return super().perform_destroy(instance)