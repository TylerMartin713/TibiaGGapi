from django.db import models
from django.contrib.auth.models import User
from .comment import Comment
from .location import Location


class Hunting_Place(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hunting_places"
    )
    recommended_level = models.IntegerField()
    raw_exp = models.IntegerField(help_text="Raw experience per hour")
    est_profit = models.IntegerField(help_text="Estimated profit per hour")
    comment = models.ForeignKey(
        Comment, on_delete=models.SET_NULL, null=True, blank=True
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hunting_place"
        verbose_name = "Hunting Place"
        verbose_name_plural = "Hunting Places"

    def __str__(self):
        return f"{self.location} - Level {self.recommended_level}"
