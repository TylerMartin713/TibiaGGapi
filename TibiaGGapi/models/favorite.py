from django.db import models
from django.contrib.auth.models import User
from .huntingplace import Hunting_Place


class Favorite(models.Model):
    """Model for user's favorited hunting places"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    hunting_place = models.ForeignKey(
        Hunting_Place, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorite"
        unique_together = ("user", "hunting_place")  # Prevent duplicate favorites
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user.username} favorites {self.hunting_place.location.name}"
