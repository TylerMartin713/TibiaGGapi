from django.db import models


class Vocation(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "vocation"
        verbose_name = "Vocation"
        verbose_name_plural = "Vocations"

    def __str__(self):
        return self.name
