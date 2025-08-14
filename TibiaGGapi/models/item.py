from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "item"
        ordering = ["name"]
