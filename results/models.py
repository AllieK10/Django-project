from django.db import models
from main.models import Task
from django.contrib.auth.models import User


class Result(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE) #we have topic field in here
    user = models.ForeignKey(User, on_delete=models.CASCADE) #to identify the user that's taking a test (id)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)
