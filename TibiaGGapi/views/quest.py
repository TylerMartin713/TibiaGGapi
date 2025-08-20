from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny
from TibiaGGapi.models import (
    Quest,
    QuestMission,
    QuestReward,
    QuestQuestReward,
    QuestDanger,
)
from django.core.exceptions import ValidationError
from django.db import transaction
import json


class QuestView(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        """Get all quests"""
        try:
            quests = Quest.objects.all()
            quest_list = []

            for quest in quests:
                quest_data = {
                    "id": quest.id,
                    "name": quest.name,
                    "description": quest.description,
                    "min_level": quest.min_level,
                    "rec_level": quest.rec_level,
                    "quest_type": quest.quest_type,
                    "difficulty_rating": quest.difficulty_rating,
                    "estimated_duration": quest.estimated_duration,
                    "prerequisites": quest.prerequisites,
                    "location": quest.location,
                    "npc_start": quest.npc_start,
                    "image_url": quest.image_url,
                    "is_premium": quest.is_premium,
                    "created_at": quest.created_at,
                    "updated_at": quest.updated_at,
                }
                quest_list.append(quest_data)

            return Response(quest_list)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Get a single quest with all missions and rewards"""
        try:
            quest = Quest.objects.get(pk=pk)

            # Get missions
            missions = QuestMission.objects.filter(quest=quest).order_by(
                "mission_order"
            )
            missions_data = []
            for mission in missions:
                mission_data = {
                    "id": mission.id,
                    "name": mission.name,
                    "description": mission.description,
                    "objective": mission.objective,
                    "mission_order": mission.mission_order,
                    "steps": mission.steps,
                    "location": mission.location,
                    "required_items": mission.required_items,
                    "notes": mission.notes,
                    "dangers": mission.dangers,
                }
                missions_data.append(mission_data)

            # Get rewards
            quest_rewards = (
                QuestQuestReward.objects.filter(quest=quest)
                .select_related("reward")
                .order_by("reward_order")
            )
            rewards_data = []
            for quest_reward in quest_rewards:
                reward_data = {
                    "id": quest_reward.reward.id,
                    "name": quest_reward.reward.name,
                    "description": quest_reward.reward.description,
                    "reward_type": quest_reward.reward.reward_type,
                    "value": quest_reward.reward.value,
                    "image_url": quest_reward.reward.image_url,
                    "is_final_reward": quest_reward.is_final_reward,
                    "mission_id": (
                        quest_reward.mission.id if quest_reward.mission else None
                    ),
                }
                rewards_data.append(reward_data)

            # Get dangers
            dangers = QuestDanger.objects.filter(quest=quest)
            dangers_data = []
            for danger in dangers:
                danger_data = {
                    "creature_name": danger.creature_name,
                    "location": danger.location,
                    "notes": danger.notes,
                }
                dangers_data.append(danger_data)

            quest_data = {
                "id": quest.id,
                "name": quest.name,
                "description": quest.description,
                "min_level": quest.min_level,
                "rec_level": quest.rec_level,
                "quest_type": quest.quest_type,
                "difficulty_rating": quest.difficulty_rating,
                "estimated_duration": quest.estimated_duration,
                "prerequisites": quest.prerequisites,
                "location": quest.location,
                "npc_start": quest.npc_start,
                "image_url": quest.image_url,
                "is_premium": quest.is_premium,
                "missions": missions_data,
                "rewards": rewards_data,
                "dangers": dangers_data,
                "created_at": quest.created_at,
                "updated_at": quest.updated_at,
            }

            return Response(quest_data)
        except Quest.DoesNotExist:
            return Response(
                {"error": "Quest not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Create a new quest"""
        try:
            with transaction.atomic():
                # Create the quest
                quest_data = request.data.get("quest", {})
                quest = Quest.objects.create(
                    name=quest_data.get("name"),
                    description=quest_data.get("description", ""),
                    min_level=quest_data.get("min_level"),
                    rec_level=quest_data.get("rec_level"),
                    quest_type=quest_data.get("quest_type", "main"),
                    difficulty_rating=quest_data.get("difficulty_rating"),
                    estimated_duration=quest_data.get("estimated_duration"),
                    prerequisites=quest_data.get("prerequisites"),
                    location=quest_data.get("location"),
                    npc_start=quest_data.get("npc_start"),
                    image_url=quest_data.get("image_url"),
                    is_premium=quest_data.get("is_premium", False),
                )

                # Create missions if provided
                missions_data = request.data.get("missions", [])
                for mission_data in missions_data:
                    QuestMission.objects.create(
                        quest=quest,
                        name=mission_data.get("name"),
                        description=mission_data.get("description", ""),
                        objective=mission_data.get("objective"),
                        mission_order=mission_data.get("mission_order"),
                        steps=mission_data.get("steps", ""),
                        location=mission_data.get("location"),
                        required_items=mission_data.get("required_items"),
                        notes=mission_data.get("notes"),
                        dangers=mission_data.get("dangers"),
                    )

                # Create rewards if provided
                rewards_data = request.data.get("rewards", [])
                for reward_data in rewards_data:
                    reward, created = QuestReward.objects.get_or_create(
                        name=reward_data.get("name"),
                        defaults={
                            "description": reward_data.get("description", ""),
                            "reward_type": reward_data.get("reward_type"),
                            "value": reward_data.get("value"),
                            "image_url": reward_data.get("image_url"),
                        },
                    )

                    QuestQuestReward.objects.create(
                        quest=quest,
                        reward=reward,
                        reward_order=reward_data.get("reward_order", 0),
                        is_final_reward=reward_data.get("is_final_reward", False),
                    )

                # Create dangers if provided
                dangers_data = request.data.get("dangers", [])
                for danger_data in dangers_data:
                    QuestDanger.objects.create(
                        quest=quest,
                        creature_name=danger_data.get("creature_name"),
                        location=danger_data.get("location"),
                        notes=danger_data.get("notes"),
                    )

                return Response(
                    {"id": quest.id, "message": "Quest created successfully"},
                    status=status.HTTP_201_CREATED,
                )

        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a quest"""
        try:
            quest = Quest.objects.get(pk=pk)
            quest.delete()
            return Response({"message": "Quest deleted successfully"})
        except Quest.DoesNotExist:
            return Response(
                {"error": "Quest not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)
