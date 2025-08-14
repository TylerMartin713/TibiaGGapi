from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item Objects"""

    class Meta:
        model = Item
        fields = ["id", "name", "image_url"]
        read_only_fields = ["id"]


class ItemViewSet(ViewSet):
    """Viewset for Items"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all items"""
        try:
            items = Item.objects.all().order_by("name")
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single item"""
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response(
                {"message": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new Item"""
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Update a Item"""
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response(
                {"message": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Delete an Item"""
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return Response(
                {"message": "Item deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Item.DoesNotExist:
            return Response(
                {"message": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)
