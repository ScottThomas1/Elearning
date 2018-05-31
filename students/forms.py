from django import forms

from courses.models import Course
from students.models import Comment


class PublicSettingsForm(forms.Form):
    display_scores = forms.BooleanField(required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 7,
                                                           'cols': 60,
                                                           'style': 'resize:none;'}))

    def __init__(self, course, student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course
        self.student = student
        if student.public_courses.exists():
            self.fields['display_scores'].initial = True
        elif student.student_comment.exists():
            self.fields['comment'].initial = True

    def save(self):
        display_scores = self.cleaned_data.get('display_scores', False)
        comment = self.cleaned_data.get('comment', '')
        print(comment)
        if comment:
            Comment.objects.create(student=self.student, text=comment, course=self.course)
        if display_scores and comment:
            self.course.public_students.add(self.student)
        else:
            self.course.public_students.remove(self.student)


# class Comment(forms.ModelForm):
#
#     class Meta:
#         model = Course
#         fields = ('student_comment',)
#
#     def __init__(self, *args, **kwargs):
#         if 'student' in kwargs:
#             student = kwargs.pop('student')
#         else:
#             student = None
#         super().__init__(*args, **kwargs)
#         if student is not None and student.public_courses.exists():
#             self.fields['student_comment'].initial = True
