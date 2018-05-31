from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

# from students.forms import Comment
from students.forms import PublicSettingsForm
from students.models import User, Comment

from courses.models import Course, UserAnswer, User, Answer
from courses.views import calculate_score
import datetime

from django.views.generic.base import TemplateView


def get_all_scores_for_user(user, taken_only=True):
    scores = []
    # ^ empty list called scores
    courses = Course.objects.filter(students=user)
    if taken_only:
        courses = courses.filter(section__questions__useranswers__user=user).distinct()
    for course in courses:
        # ^ gets the course of the Model Course as well as the objects and
        # ^ filters them by student now called 'user'
        course_data = {'course': course}
        # ^ inserting course to a dict
        sections = []
        # ^ empty list called sections
        section_qs = course.section_set.order_by('number')
        if taken_only:
            section_qs = section_qs.filter(questions__useranswers__user=user).distinct()
        for section in section_qs:
            # ^ looping through all sections in course
            # ^ doing a reverse lookup on section (section_set) and ordering
            # ^ them the the number on the Section model
            has_taken = UserAnswer.objects.filter(user=user, question__section=section).order_by('test_was_taken').first()
            section_data = {
                'score': calculate_score(user, section),
                'section': section,
            }
            if has_taken is not None:
                section_data['test_was_taken'] = has_taken.test_was_taken
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
    if not request.user.is_authenticated:
        raise PermissionDenied
    student = request.user
    return render(request, 'students/student_detail.html', {
        'student': student,
        'scores': get_all_scores_for_user(student),
    })


@login_required
def student_page(request):
    student = request.user
    courses = Course.objects.filter(students=student)
    return render(request, 'students/student_page.html', {
        'student': student,
        'courses': courses,
        'scores': get_all_scores_for_user(student, taken_only=False)
     })


def public_page(request):
    courses = []
    for course in Course.objects.all():
        course_data = {'course': course}
        sections = []
        for section in course.section_set.all():
            section_data = {'section': section}
            students = []
            for student in course.public_students.all():
                student_data = {'student': student}
                student_data['score'] = calculate_score(student, section)
                first_answer = UserAnswer.objects.filter(
                    user=student, question__section=section).order_by(
                    'test_was_taken').first()
                if first_answer is not None:
                    student_data['test_was_taken'] = first_answer.test_was_taken
                students.append(student_data)
            section_data['students'] = students
            sections.append(section_data)
        course_data['sections'] = sections
        courses.append(course_data)
    comments = Comment.objects.all()
    return render(request, 'students/public_page.html', {
        'comments': comments,
        'courses': courses,
    })
