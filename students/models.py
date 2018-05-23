from django.contrib.auth.models import AbstractUser
from django.db import models
# from courses.models import Course


class User(AbstractUser):
    pass


class Comment(models.Model):
    # student_comment = models.ForeignKey(Course)
    student = models.ForeignKey(User)
    text = models.CharField(max_length=600)

    def __str__(self):
        return self.text
