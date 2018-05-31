from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Comment(models.Model):
    course = models.ForeignKey('courses.Course')
    student = models.ForeignKey(User)
    text = models.CharField(max_length=600)

    def __str__(self):
        return self.text
