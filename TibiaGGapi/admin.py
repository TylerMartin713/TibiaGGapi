from django.contrib import admin
from .models import (
    Hunting_Place,
    Hunting_Place_Comment,
    Location,
    Comment,
    Vocation,
    Character,
    Creature,
    Imbue,
    Item,
    Favorite,
    Quest,
    QuestMission,
    QuestReward,
    QuestQuestReward,
    QuestDanger,
)

# Register your models here.


# Quest Admin Classes
class QuestMissionInline(admin.TabularInline):
    model = QuestMission
    extra = 1
    ordering = ["mission_order"]


class QuestQuestRewardInline(admin.TabularInline):
    model = QuestQuestReward
    extra = 1
    ordering = ["reward_order"]


class QuestDangerInline(admin.TabularInline):
    model = QuestDanger
    extra = 1


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "quest_type",
        "min_level",
        "rec_level",
        "is_premium",
        "created_at",
    ]
    list_filter = ["quest_type", "is_premium", "difficulty_rating"]
    search_fields = ["name", "description", "location"]
    inlines = [QuestMissionInline, QuestQuestRewardInline, QuestDangerInline]
    ordering = ["name"]


@admin.register(QuestMission)
class QuestMissionAdmin(admin.ModelAdmin):
    list_display = ["name", "quest", "mission_order", "location"]
    list_filter = ["quest", "location"]
    search_fields = ["name", "objective", "description"]
    ordering = ["quest", "mission_order"]


@admin.register(QuestReward)
class QuestRewardAdmin(admin.ModelAdmin):
    list_display = ["name", "reward_type", "value"]
    list_filter = ["reward_type"]
    search_fields = ["name", "description"]
    ordering = ["reward_type", "name"]


@admin.register(QuestQuestReward)
class QuestQuestRewardAdmin(admin.ModelAdmin):
    list_display = ["quest", "reward", "mission", "is_final_reward"]
    list_filter = ["is_final_reward", "quest"]
    ordering = ["quest", "reward_order"]


@admin.register(QuestDanger)
class QuestDangerAdmin(admin.ModelAdmin):
    list_display = ["quest", "creature_name", "location"]
    list_filter = ["quest", "creature_name"]
    search_fields = ["creature_name", "location"]
    ordering = ["quest", "creature_name"]
