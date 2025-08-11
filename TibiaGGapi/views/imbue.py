from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Imbue


class ImbueSerializer(serializers.ModelSerializer):
    """Serializer for Imbue objects"""

    class Meta:
        model = Imbue
        fields = ["id", "name", "image"]
        read_only_fields = ["id"]


class ImbueViewSet(ViewSet):
    """Viewset for imbues"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all imbues"""
        try:
            imbues = Imbue.objects.all().order_by("name")
            serializer = ImbueSerializer(imbues, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single imbue"""
        try:
            imbue = Imbue.objects.get(pk=pk)
            serializer = ImbueSerializer(imbue)
            return Response(serializer.data)
        except Imbue.DoesNotExist:
            return Response(
                {"message": "Imbue not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new imbue"""
        try:
            serializer = ImbueSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Update a imbue"""
        try:
            imbue = Imbue.objects.get(pk=pk)
            serializer = ImbueSerializer(imbue, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Imbue.DoesNotExist:
            return Response(
                {"message": "Imbue not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Delete a imbue"""
        try:
            imbue = Imbue.objects.get(pk=pk)
            imbue.delete()
            return Response(
                {"message": "Imbue deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Imbue.DoesNotExist:
            return Response(
                {"message": "Imbue not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)
