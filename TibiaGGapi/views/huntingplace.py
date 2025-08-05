from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Hunting_Place, Location, Comment


class HuntingPlaceSerializer(serializers.ModelSerializer):
    """Serializer for hunting place objects"""

    location_name = serializers.CharField(source="location.name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    comment_description = serializers.CharField(
        source="comment.description", read_only=True
    )

    class Meta:
        model = Hunting_Place
        fields = [
            "id",
            "user",
            "user_username",
            "recommended_level",
            "raw_exp",
            "est_profit",
            "comment",
            "comment_description",
            "location",
            "location_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]


class HuntingPlaceViewSet(ViewSet):
    """ViewSet for hunting places"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all hunting places"""
        try:
            hunting_places = Hunting_Place.objects.select_related(
                "user", "location", "comment"
            ).all()
            serializer = HuntingPlaceSerializer(hunting_places, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single hunting place"""
        try:
            hunting_place = Hunting_Place.objects.select_related(
                "user", "location", "comment"
            ).get(pk=pk)
            serializer = HuntingPlaceSerializer(hunting_place)
            return Response(serializer.data)
        except Hunting_Place.DoesNotExist:
            return Response(
                {"message": "Hunting place not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new hunting place"""
        try:
            serializer = HuntingPlaceSerializer(data=request.data)
            if serializer.is_valid():
                # Automatically set the user to the current authenticated user
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Update a hunting place"""
        try:
            hunting_place = Hunting_Place.objects.get(pk=pk)

            # Only allow the owner to update their hunting place
            if hunting_place.user != request.user:
                return Response(
                    {"message": "You can only edit your own hunting places"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = HuntingPlaceSerializer(hunting_place, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Hunting_Place.DoesNotExist:
            return Response(
                {"message": "Hunting place not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Delete a hunting place"""
        try:
            hunting_place = Hunting_Place.objects.get(pk=pk)

            # Only allow the owner to delete their hunting place
            if hunting_place.user != request.user:
                return Response(
                    {"message": "You can only delete your own hunting places"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            hunting_place.delete()
            return Response(
                {"message": "Hunting place deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Hunting_Place.DoesNotExist:
            return Response(
                {"message": "Hunting place not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def my_hunting_places(self, request):
        """Get hunting places created by the current user"""
        try:
            hunting_places = Hunting_Place.objects.select_related(
                "user", "location", "comment"
            ).filter(user=request.user)
            serializer = HuntingPlaceSerializer(hunting_places, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def by_level(self, request):
        """Get hunting places filtered by level range"""
        try:
            min_level = request.query_params.get("min_level")
            max_level = request.query_params.get("max_level")

            hunting_places = Hunting_Place.objects.select_related(
                "user", "location", "comment"
            ).all()

            if min_level:
                hunting_places = hunting_places.filter(recommended_level__gte=min_level)
            if max_level:
                hunting_places = hunting_places.filter(recommended_level__lte=max_level)

            serializer = HuntingPlaceSerializer(hunting_places, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def by_profit(self, request):
        """Get hunting places filtered by minimum profit"""
        try:
            min_profit = request.query_params.get("min_profit", 0)

            hunting_places = (
                Hunting_Place.objects.select_related("user", "location", "comment")
                .filter(est_profit__gte=min_profit)
                .order_by("-est_profit")
            )

            serializer = HuntingPlaceSerializer(hunting_places, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
