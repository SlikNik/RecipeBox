from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_time = models.CharField(max_length=100)
    instructions = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    favorites = models.ManyToManyField(User, blank=True,
                                       related_name="favorites")

    def __str__(self):
        return f"{self.title} by {self.author.name}"