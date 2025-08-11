from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Creature


class CreatureSerializer(serializers.ModelSerializer):
    """Serializer for creature objects"""

    class Meta:
        model = Creature
        fields = [
            "id",
            "name",
            "hitpoints",
            "experience_points",
            "image_url",
            "last_updated",
        ]
        read_only_fields = ["id", "last_updated"]


class CreatureViewSet(ViewSet):
    """ViewSet for creatures"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all creatures"""
        try:
            creatures = Creature.objects.all().order_by("name")
            serializer = CreatureSerializer(creatures, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single creature"""
        try:
            creature = Creature.objects.get(pk=pk)
            serializer = CreatureSerializer(creature)
            return Response(serializer.data)
        except Creature.DoesNotExist:
            return Response(
                {"message": "Creature not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new creature"""
        try:
            serializer = CreatureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Update a creature"""
        try:
            creature = Creature.objects.get(pk=pk)
            serializer = CreatureSerializer(creature, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Creature.DoesNotExist:
            return Response(
                {"message": "Creature not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Delete a creature"""
        try:
            creature = Creature.objects.get(pk=pk)
            creature.delete()
            return Response(
                {"message": "Creature deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Creature.DoesNotExist:
            return Response(
                {"message": "Creature not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search creatures by name"""
        try:
            query = request.query_params.get("q", "")
            if query:
                creatures = Creature.objects.filter(name__icontains=query).order_by(
                    "name"
                )
            else:
                creatures = Creature.objects.all().order_by("name")

            serializer = CreatureSerializer(creatures, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def by_hitpoints(self, request):
        """Get creatures filtered by hitpoint range"""
        try:
            min_hp = request.query_params.get("min_hp")
            max_hp = request.query_params.get("max_hp")

            creatures = Creature.objects.all()

            if min_hp:
                creatures = creatures.filter(hitpoints__gte=min_hp)
            if max_hp:
                creatures = creatures.filter(hitpoints__lte=max_hp)

            creatures = creatures.order_by("hitpoints", "name")
            serializer = CreatureSerializer(creatures, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def by_experience(self, request):
        """Get creatures filtered by experience points"""
        try:
            min_exp = request.query_params.get("min_exp", 0)

            creatures = Creature.objects.filter(
                experience_points__gte=min_exp
            ).order_by("-experience_points", "name")

            serializer = CreatureSerializer(creatures, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def high_value_targets(self, request):
        """Get creatures with high experience per hitpoint ratio"""
        try:
            creatures = Creature.objects.all()

            # Calculate experience per hitpoint ratio and filter high-value targets
            high_value_creatures = []
            for creature in creatures:
                if creature.hitpoints > 0:  # Avoid division by zero
                    exp_per_hp = creature.experience_points / creature.hitpoints
                    if exp_per_hp >= 1:  # At least 1 exp per HP
                        high_value_creatures.append(creature)

            # Sort by experience points descending
            high_value_creatures.sort(key=lambda x: x.experience_points, reverse=True)

            serializer = CreatureSerializer(high_value_creatures, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def weak_creatures(self, request):
        """Get creatures with low hitpoints (good for low-level hunting)"""
        try:
            max_hp = request.query_params.get("max_hp", 500)

            creatures = Creature.objects.filter(hitpoints__lte=max_hp).order_by(
                "hitpoints", "-experience_points"
            )

            serializer = CreatureSerializer(creatures, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
