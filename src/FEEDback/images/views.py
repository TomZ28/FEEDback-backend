from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from images.models import RestaurantImage
from images.serializers import RestaurantImageSerializer
from restaurants.permissions import IsRestaurantOwner

# Create your views here.

class DeleteImageView(DestroyAPIView):
    """
    Delete the RestaurantImage with the given id, if it exists. Requires that
    the user is authenticated and owns the restaurant that added the RestaurantImage.
    """
    permission_classes = (IsAuthenticated, IsRestaurantOwner)
    serializer_class = RestaurantImageSerializer
    lookup_field = 'id'
    queryset = RestaurantImage.objects.all()

    def perform_destroy(self, instance):
        image = get_object_or_404(RestaurantImage, id=self.kwargs['id'])

        # Check if current user owns restaurant
        self.check_object_permissions(self.request, image.restaurant)

        return super().perform_destroy(instance)