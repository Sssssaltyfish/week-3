import ast
from django.db import models

# Create your models here.
class Actor(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    url = models.URLField()
    summary = models.TextField()
    cover = models.URLField()
    info = models.TextField()
    relations = models.ManyToManyField(
        'self',
        blank=True,
        through='RelationShip',
        through_fields=('first_actor', 'second_actor'),
        symmetrical=False
    )

    def get_info(self):
        return ast.literal_eval(self.info).items()

    def __str__(self) -> str:
        return self.name


class Relationship(models.Model):
    first_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    second_actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.first_actor} - {self.second_actor}: {self.count}'


class Movie(models.Model):
    title = models.CharField(primary_key=True, max_length=30)
    cover = models.URLField()
    actors = models.ManyToManyField(Actor, blank=True)
    summary = models.TextField()
    comments = models.TextField()

    def __str__(self) -> str:
        return self.title

    def get_comments(self):
        return ast.literal_eval(self.comments)