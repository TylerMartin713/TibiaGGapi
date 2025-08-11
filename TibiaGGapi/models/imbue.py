from django.db import models


class Imbue(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()

    class Meta:
        db_table = "imbue"
        verbose_name = "Imbue"
        verbose_name_plural = "Imbues"

    def __str__(self):
        return self.name
