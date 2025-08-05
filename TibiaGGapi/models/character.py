from django.db import models
from django.utils import timezone


class Character(models.Model):
    name = models.CharField(max_length=100, unique=True)
    vocation = models.CharField(max_length=50)
    level = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "character"
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def is_fresh(self):
        return (timezone.now() - self.last_updated).total_seconds() < 600  # 10 minutes

    def __str__(self):
        return f"{self.name} - {self.vocation} (Level {self.level})"
