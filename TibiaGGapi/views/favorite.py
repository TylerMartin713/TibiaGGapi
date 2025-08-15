from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Favorite, Hunting_Place
from .huntingplace import HuntingPlaceSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorite objects"""

    hunting_place = HuntingPlaceSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "hunting_place", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class FavoriteViewSet(ViewSet):
    """Viewset for Favorites"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all favorites for the current user"""
        try:
            favorites = Favorite.objects.filter(user=request.user).order_by(
                "-created_at"
            )
            serializer = FavoriteSerializer(favorites, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Add a hunting place to favorites"""
        try:
            hunting_place_id = request.data.get("hunting_place_id")

            if not hunting_place_id:
                return Response(
                    {"error": "hunting_place_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                hunting_place = Hunting_Place.objects.get(id=hunting_place_id)
            except Hunting_Place.DoesNotExist:
                return Response(
                    {"error": "Hunting place not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Check if already favorited
            if Favorite.objects.filter(
                user=request.user, hunting_place=hunting_place
            ).exists():
                return Response(
                    {"error": "Already favorited"}, status=status.HTTP_400_BAD_REQUEST
                )

            favorite = Favorite.objects.create(
                user=request.user, hunting_place=hunting_place
            )

            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Remove a hunting place from favorites"""
        try:
            favorite = Favorite.objects.get(pk=pk, user=request.user)
            favorite.delete()
            return Response(
                {"message": "Removed from favorites"}, status=status.HTTP_204_NO_CONTENT
            )
        except Favorite.DoesNotExist:
            return Response(
                {"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        """Toggle favorite status for a hunting place"""
        try:
            hunting_place_id = request.data.get("hunting_place_id")

            if not hunting_place_id:
                return Response(
                    {"error": "hunting_place_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                hunting_place = Hunting_Place.objects.get(id=hunting_place_id)
            except Hunting_Place.DoesNotExist:
                return Response(
                    {"error": "Hunting place not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            favorite = Favorite.objects.filter(
                user=request.user, hunting_place=hunting_place
            ).first()

            if favorite:
                # Remove from favorites
                favorite.delete()
                return Response(
                    {"favorited": False, "message": "Removed from favorites"}
                )
            else:
                # Add to favorites
                favorite = Favorite.objects.create(
                    user=request.user, hunting_place=hunting_place
                )
                serializer = FavoriteSerializer(favorite)
                return Response(
                    {
                        "favorited": True,
                        "message": "Added to favorites",
                        "favorite": serializer.data,
                    }
                )

        except Exception as ex:
            return HttpResponseServerError(ex)
