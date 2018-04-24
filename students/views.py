from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from students.models import User

from courses.models import Course, UserAnswer, User, Answer
from courses.views import calculate_score
import datetime

from django.views.generic.base import TemplateView


def get_all_scores_for_user(user):
    scores = []
    # ^ empty list called scores
    for course in Course.objects.filter(students=user):
        # ^ gets the course of the Model Course as well as the objects and
        # ^ filters them by student now called 'user'
        course_data = {'course': course}
        # ^ inserting course to a dict
        sections = []
        # ^ empty list called sections
        for section in course.section_set.order_by('number'):
            # ^ looping through all sections in course
            # ^ doing a reverse lookup on section (section_set) and ordering
            # ^ them the the number on the Section model
            section_data = {'score': calculate_score(user, section), 'section': section}
            # ^ inserting calculate_score, user and section into key 'score' and section into 'section'
            questions = []
            # ^ empty list called questions
            for question in section.questions.all():
                # ^ looping through every question in sections in the course
                question_data = {'correct_answer': question.answers.filter(correct=True), 'question': question}
                # ^ inserting question.answers.filter(correct=True) into
                # ^ inserting list of correct answers
                try:
                    # ^ try to do the following
                    useranswer = question.useranswers.get(user=user)
                    # ^ useranswer is getting the useranswer of that user
                except UserAnswer.DoesNotExist:
                    # ^ unless User didn't answer question
                    useranswer = None
                    # ^ useranswer is None (blank)
                if useranswer is not None and useranswer.answer in question_data['correct_answer']:
                    # ^ looking to see if useranswer wasn't left blank and
                    # ^ useranswer.(lookup) answer is in question_data in the qeryset
                    # ^ (functions like a list) 'correct_answer'
                    question_data['correct'] = useranswer
                    # ^ if useranswer is not None and useranswer is in list then useranswer is True
                else:
                    # ^
                    question_data['incorrect'] = useranswer
                    # ^ if useranswer is None or useranswer is not in list
                question_data['useranswer'] = useranswer
                # ^ question_data with list 'useranswer' is useranswer
                questions.append(question_data)
                # ^ adding question_data  to questions
            section_data['questions'] = questions
            # ^ section_data with list 'questions' is questions
            sections.append(section_data)
            # ^ adding section_data to sections
        course_data['sections'] = sections
        # ^ course_data with list 'sections' is sections
        scores.append(course_data)
        # ^ (could you use extend() to add all appended items to course_data?)
    return scores
    # ^ return everything that is in score list []


def student_detail(request):
    if not request.user.is_authenticated():
        raise PermissionDenied
    student = request.user
    now = datetime.datetime.now()
    return render(request, 'students/student_detail.html', {
        'now': now,
        'student': student,
        'scores': get_all_scores_for_user(student),
    })


@login_required
def student_page(request):
    student = request.user
    courses = Course.objects.filter(students=student)
    return render(request, 'students/student_page.html', {
        'student': student,
        'courses': courses
     })



