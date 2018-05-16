from django import forms

from courses.models import Course


class PublicSettingsForm(forms.Form):
    display_scores = forms.BooleanField(required=False)
    test = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        if 'student' in kwargs:
            student = kwargs.pop('student')
        else:
            student=None
        super().__init__(*args, **kwargs)
        if student is not None and student.public_courses.exists():
            self.fields['display_scores'].initial = True

    def save(self, student):
        display_scores = self.cleaned_data.get('display_scores', False)
        for course in Course.objects.all():
            if display_scores:
                course.public_students.add(student)
            else:
                course.public_students.remove(student)

