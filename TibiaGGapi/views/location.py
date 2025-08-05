from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for location objects"""

    class Meta:
        model = Location
        fields = ["id", "name"]
        read_only_fields = ["id"]


class LocationViewSet(ViewSet):
    """ViewSet for locations"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all locations"""
        try:
            locations = Location.objects.all().order_by("name")
            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single location"""
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response(
                {"message": "Location not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new location"""
        try:
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Update a location"""
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response(
                {"message": "Location not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Delete a location"""
        try:
            location = Location.objects.get(pk=pk)
            location.delete()
            return Response(
                {"message": "Location deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Location.DoesNotExist:
            return Response(
                {"message": "Location not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search locations by name"""
        try:
            query = request.query_params.get("q", "")
            if query:
                locations = Location.objects.filter(name__icontains=query).order_by(
                    "name"
                )
            else:
                locations = Location.objects.all().order_by("name")

            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=True, methods=["get"])
    def hunting_places(self, request, pk=None):
        """Get all hunting places for this location"""
        try:
            from TibiaGGapi.models import Hunting_Place
            from TibiaGGapi.views.huntingplace import HuntingPlaceSerializer

            location = Location.objects.get(pk=pk)
            hunting_places = Hunting_Place.objects.select_related(
                "user", "location", "comment"
            ).filter(location=location)

            serializer = HuntingPlaceSerializer(hunting_places, many=True)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response(
                {"message": "Location not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)
