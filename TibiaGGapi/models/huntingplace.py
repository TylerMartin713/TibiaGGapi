from django.db import models
from django.contrib.auth.models import User
from .comment import Comment
from .location import Location
from .vocation import Vocation
from .creature import Creature
from .imbue import Imbue


class Hunting_Place(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hunting_places"
    )
    description = models.TextField(
        help_text="Detailed description of the hunting place", blank=True, null=True
    )
    recommended_level = models.IntegerField()
    raw_exp = models.IntegerField(help_text="Raw experience per hour")
    est_profit = models.IntegerField(help_text="Estimated profit per hour")
    recommended_vocation = models.ForeignKey(
        Vocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Best vocation for this hunting place",
    )
    creatures = models.ManyToManyField(
        Creature,
        related_name="hunting_places",
        help_text="Creatures found in this hunting place",
    )
    imbues = models.ManyToManyField(
        Imbue,
        related_name="hunting_places",
        blank=True,
        help_text="Recommended imbues for this hunting place",
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hunting_place"
        verbose_name = "Hunting Place"
        verbose_name_plural = "Hunting Places"

    def __str__(self):
        return f"{self.location.name} - Level {self.recommended_level}"


class Hunting_Place_Comment(models.Model):
    hunting_place = models.ForeignKey(
        Hunting_Place, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hunting_place_comments"
    )
    comment = models.TextField(help_text="User comment about the hunting place")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hunting_place_comment"
        verbose_name = "Hunting Place Comment"
        verbose_name_plural = "Hunting Place Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.hunting_place.location.name}"
