from django.shortcuts import get_object_or_404
from TibiaGGapi.models import Character, Creature
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests


@api_view(["GET"])
def get_character_info(request, name):
    try:
        char = Character.objects.get(name__iexact=name)

        if char.is_fresh():
            # Return our clean data structure
            return Response(
                {
                    "name": char.name,
                    "vocation": char.vocation,
                    "level": char.level,
                    "last_updated": char.last_updated,
                }
            )

    except Character.DoesNotExist:
        char = None

    # If not in DB or stale, fetch from TibiaData
    url = f"https://api.tibiadata.com/v4/character/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract only the fields we need from TibiaData response
        try:
            character_data = data.get("character", {})
            character_info = character_data.get("character", {})

            extracted_name = character_info.get("name", "")
            extracted_vocation = character_info.get("vocation", "")
            extracted_level = character_info.get("level", 0)

            if char:
                # Update existing character
                char.name = extracted_name
                char.vocation = extracted_vocation
                char.level = extracted_level
                char.last_updated = timezone.now()
                char.save()
            else:
                # Create new character
                char = Character.objects.create(
                    name=extracted_name,
                    vocation=extracted_vocation,
                    level=extracted_level,
                )

            # Return our clean data structure
            return Response(
                {
                    "name": char.name,
                    "vocation": char.vocation,
                    "level": char.level,
                    "last_updated": char.last_updated,
                }
            )

        except KeyError as e:
            return Response(
                {"error": f"Failed to extract character data: {str(e)}"}, status=400
            )
    else:
        return Response({"error": "Character not found"}, status=404)


@api_view(["GET"])
def get_creature_info(request, name):
    try:
        creature = Creature.objects.get(name__iexact=name)

        if creature.is_fresh():
            # Return our clean data structure
            return Response(
                {
                    "name": creature.name,
                    "hitpoints": creature.hitpoints,
                    "experience_points": creature.experience_points,
                    "image_url": creature.image_url,
                    "last_updated": creature.last_updated,
                }
            )

    except Creature.DoesNotExist:
        creature = None

    # If not in DB or stale, fetch from TibiaData
    url = f"https://api.tibiadata.com/v4/creature/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract only the fields we need from TibiaData response
        try:
            creature_data = data.get("creature", {})

            extracted_name = creature_data.get("name", "")
            extracted_hitpoints = creature_data.get("hitpoints", 0)
            extracted_experience = creature_data.get("experience_points", 0)
            extracted_image_url = creature_data.get("image_url", "")

            if creature:
                # Update existing creature
                creature.name = extracted_name
                creature.hitpoints = extracted_hitpoints
                creature.experience_points = extracted_experience
                creature.image_url = extracted_image_url
                creature.last_updated = timezone.now()
                creature.save()
            else:
                # Create new creature
                creature = Creature.objects.create(
                    name=extracted_name,
                    hitpoints=extracted_hitpoints,
                    experience_points=extracted_experience,
                    image_url=extracted_image_url,
                )

            # Return our clean data structure
            return Response(
                {
                    "name": creature.name,
                    "hitpoints": creature.hitpoints,
                    "experience_points": creature.experience_points,
                    "image_url": creature.image_url,
                    "last_updated": creature.last_updated,
                }
            )

        except KeyError as e:
            return Response(
                {"error": f"Failed to extract creature data: {str(e)}"}, status=400
            )
    else:
        return Response({"error": "Creature not found"}, status=404)
