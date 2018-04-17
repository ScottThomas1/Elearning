from django.db import models
from django.core.urlresolvers import reverse
from students.models import User
from django.conf import settings
# from tinymce.models import HTMLField
from tinymce import models as tinymce_models


class Course(models.Model):
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(User)
    teacher = models.CharField(max_length=20, default='teacher')
    context = tinymce_models.HTMLField(default='text')

    def get_absolute_url(self):
        return reverse('course_detail', args=(self.id,))

    def __str__(self):
        return self.name


class Section(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100)
    number = models.IntegerField()
    # context = HTMLField(default='HTML')
    context = tinymce_models.HTMLField()
    link = models.URLField()

    class Meta:
        unique_together = ('course', 'number')

    def __str__(self):
        return self.title

    def get_test_url(self):
        return reverse('do_test', args=(self.id,))

    def get_absolute_url(self):
        return reverse('do_section', kwargs={'section_id': self.id, })

    def get_next_section_url(self):
        next_section = Section.objects.get(
            number=self.number + 1, course=self.course_id
        )  # can't figure out how to use objects.filter
        return reverse('do_section', args=(next_section.id,))       # to get next section? when set to + 1


class Question(models.Model):
    section = models.ForeignKey(Section, related_name='questions')
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    text = models.CharField(max_length=1000)
    correct = models.BooleanField()

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, related_name='useranswers')
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = ('question', 'user')

    def __str__(self):
        return str(self.answer)
