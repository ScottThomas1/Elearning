from django.contrib import admin
from courses.models import Course, Section, Question, Answer, UserAnswer


class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)


class SectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Section, SectionAdmin)


class QuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Answer, AnswerAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'answer']
    list_filter = ['question__section']


admin.site.register(UserAnswer, UserAnswerAdmin)
