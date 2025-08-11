from django.db import models


class Vocation(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = "vocation"
        verbose_name = "Vocation"
        verbose_name_plural = "Vocations"

    def __str__(self):
        return self.name
