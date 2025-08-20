from django.db import models
from .location import Location


class Quest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    min_level = models.IntegerField(null=True, blank=True)
    rec_level = models.IntegerField(null=True, blank=True)
    quest_type = models.CharField(
        max_length=50, default="main"
    )  # main, side, daily, etc.
    difficulty_rating = models.IntegerField(null=True, blank=True)  # 1-5 scale
    estimated_duration = models.CharField(max_length=100, null=True, blank=True)
    prerequisites = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    npc_start = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class QuestMission(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="missions")
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    objective = models.TextField()
    mission_order = models.IntegerField()
    steps = models.TextField()  # JSON string or detailed text
    location = models.CharField(max_length=200, null=True, blank=True)
    required_items = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    dangers = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quest.name} - {self.name}"

    class Meta:
        ordering = ["quest", "mission_order"]


class QuestReward(models.Model):
    REWARD_TYPES = [
        ("experience", "Experience Points"),
        ("money", "Gold Coins"),
        ("item", "Item"),
        ("access", "Access/Permission"),
        ("service", "Service/Feature"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    value = models.CharField(
        max_length=100, null=True, blank=True
    )  # amount or item name
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["reward_type", "name"]


class QuestQuestReward(models.Model):
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name="quest_rewards"
    )
    reward = models.ForeignKey(QuestReward, on_delete=models.CASCADE)
    mission = models.ForeignKey(
        QuestMission, on_delete=models.CASCADE, null=True, blank=True
    )  # optional - for mission-specific rewards
    reward_order = models.IntegerField(default=0)
    is_final_reward = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quest.name} - {self.reward.name}"

    class Meta:
        ordering = ["quest", "reward_order"]
        unique_together = ["quest", "reward", "mission"]


class QuestDanger(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="dangers")
    creature_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.quest.name} - {self.creature_name}"

    class Meta:
        ordering = ["quest", "creature_name"]
