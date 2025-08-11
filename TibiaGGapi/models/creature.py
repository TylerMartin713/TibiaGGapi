from django.db import models
from django.utils import timezone


class Creature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hitpoints = models.IntegerField()
    experience_points = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "creature"
        verbose_name = "Creature"
        verbose_name_plural = "Creatures"

    def is_fresh(self):
        return (timezone.now() - self.last_updated).total_seconds() < 600  # 10 minutes

    def __str__(self):
        return f"{self.name} - {self.hitpoints} HP ({self.experience_points} XP)"
