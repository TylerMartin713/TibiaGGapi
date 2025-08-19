from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from TibiaGGapi.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    """Serializer for character objects"""

    class Meta:
        model = Character
        fields = ["id", "name", "vocation", "level", "last_updated"]
        read_only_fields = ["id", "last_updated"]


class CharacterViewSet(ViewSet):
    """ViewSet for characters"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all characters"""
        try:
            characters = Character.objects.all().order_by("name")
            serializer = CharacterSerializer(characters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single character"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character)
            return Response(serializer.data)
        except Character.DoesNotExist:
            return Response(
                {"message": "Character not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new character"""
        try:
            serializer = CharacterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Update a character"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Character.DoesNotExist:
            return Response(
                {"message": "Character not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Delete a character"""
        try:
            character = Character.objects.get(pk=pk)
            character.delete()
            return Response(
                {"message": "Character deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Character.DoesNotExist:
            return Response(
                {"message": "Character not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search characters by name"""
        try:
            query = request.query_params.get("q", "")
            if query:
                characters = Character.objects.filter(name__icontains=query).order_by(
                    "name"
                )
            else:
                characters = Character.objects.all().order_by("name")

            serializer = CharacterSerializer(characters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def by_vocation(self, request):
        """Get characters filtered by vocation"""
        try:
            vocation = request.query_params.get("vocation", "")
            if vocation:
                characters = Character.objects.filter(
                    vocation__icontains=vocation
                ).order_by("level", "name")
            else:
                characters = Character.objects.all().order_by("level", "name")

            serializer = CharacterSerializer(characters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["get"])
    def by_level_range(self, request):
        """Get characters filtered by level range"""
        try:
            min_level = request.query_params.get("min_level")
            max_level = request.query_params.get("max_level")

            characters = Character.objects.all()

            if min_level:
                characters = characters.filter(level__gte=min_level)
            if max_level:
                characters = characters.filter(level__lte=max_level)

            characters = characters.order_by("-level", "name")
            serializer = CharacterSerializer(characters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(detail=False, methods=["post"])
    def search_and_add(self, request):
        """Search for a character from Tibia API and add to database"""
        try:
            import requests
            from datetime import datetime

            character_name = request.data.get("name", "").strip()
            if not character_name:
                return Response(
                    {"error": "Character name is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if character already exists in our database
            existing_character = Character.objects.filter(
                name__iexact=character_name
            ).first()
            if existing_character:
                return Response(
                    {
                        "error": f"Character '{character_name}' already exists in your database"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch character data from Tibia API
            api_url = f"https://api.tibiadata.com/v4/character/{character_name}"
            response = requests.get(api_url)

            if response.status_code != 200:
                return Response(
                    {"error": "Failed to fetch character data from Tibia API"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = response.json()

            # Check if character exists in Tibia
            if not data.get("characters") or not data["characters"].get("character"):
                return Response(
                    {"error": f"Character '{character_name}' not found in Tibia"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            char_data = data["characters"]["character"]

            # Create new character in our database
            new_character = Character.objects.create(
                name=char_data.get("name"),
                vocation=char_data.get("vocation"),
                level=char_data.get("level"),
                last_updated=datetime.now(),
            )

            serializer = CharacterSerializer(new_character)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            return Response(
                {"error": "Failed to connect to Tibia API"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as ex:
            return HttpResponseServerError(ex)
