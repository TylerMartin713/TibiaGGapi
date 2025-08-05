from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Vocation


class VocationSerializer(serializers.ModelSerializer):
    """Serializer for vocation objects"""

    class Meta:
        model = Vocation
        fields = ["id", "name"]
        read_only_fields = ["id"]


class VocationViewSet(ViewSet):
    """ViewSet for vocations"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all vocations"""
        try:
            vocations = Vocation.objects.all().order_by("name")
            serializer = VocationSerializer(vocations, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single vocation"""
        try:
            vocation = Vocation.objects.get(pk=pk)
            serializer = VocationSerializer(vocation)
            return Response(serializer.data)
        except Vocation.DoesNotExist:
            return Response(
                {"message": "Vocation not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new vocation"""
        try:
            serializer = VocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Update a Vocation"""
        try:
            vocation = Vocation.objects.get(pk=pk)
            serializer = VocationSerializer(vocation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vocation.DoesNotExist:
            return Response(
                {"message": "Vocation not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Delete a vocation"""
        try:
            vocation = Vocation.objects.get(pk=pk)
            vocation.delete()
            return Response(
                {"message": "Vocation delete successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Vocation.DoesNotExist:
            return Response(
                {"message": "Vocation not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)
