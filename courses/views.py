from django.db import transaction
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, CreateView, ListView
from django.shortcuts import render, redirect
from courses.models import Course, Section, Question, UserAnswer

from students.models import Comment, User

from django.contrib.auth.decorators import login_required

from courses.serializers import SectionSerializer

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from courses.forms import CourseForm
from students.forms import PublicSettingsForm
from django.http import HttpResponseRedirect


def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    comments = Comment.objects.filter(course=course)
    if request.user.is_authenticated:
        student = request.user
        if request.method == "POST":
            form = PublicSettingsForm(course, student, request.POST)
            if form.is_valid():
                form.save()
                # return redirect(reverse('public_page'))
        form = PublicSettingsForm(course, student)
    else:
        form = None
    return render(request, 'courses/course_detail.html', {
        'comments': comments,
        'course': course,
        'form': form
    })

# class CourseDetailView(DetailView):
#     model = Course
#     student_model = Comment
#     form = PublicSettingsForm
    # form = forms.CharField(widget=forms.Textarea(attrs={'rows': 7,
    #                                                        'cols': 60,
    #                                                        'style': 'resize:none;'}))


class CourseListView(ListView):  # LoginRequiredMixin,
    model = Course
    queryset = Course.objects.prefetch_related('students')


def course_add(request):
    if request.POST:
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save()
            return HttpResponseRedirect(new_course.get_absolute_url())
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {
        'form': form,
    })


class CourseAddView(CreateView):
    model = Course
    fields = '__all__'


course_add = CourseAddView.as_view()


def do_section(request, section_id):
    student = request.user
    # students = User.objects.all()
    if request.method == "POST":
        form = PublicSettingsForm(section_id, student, request.POST)
        if form.is_valid():
            form.save()
    form = PublicSettingsForm(section_id, student)
    section = Section.objects.get(id=section_id)
    student_data = {'student': student}
    student_data['score'] = calculate_score(student, section)
    first_answer = UserAnswer.objects.filter(
        user=student, question__section=section).order_by('test_was_taken').first()
    if first_answer is not None:
            student_data['test_was_taken'] = first_answer.test_was_taken
    return render(request, 'courses/do_section.html', {
        'student_data': student_data,
        'section': section,
        'form': form
    })


# def do_section(request, section_id):
#     courses = []
#     for course in Course.objects.all():
#         course_data = {'course': course}
#         sections = []
#         for section in course.section_set.all():
#             section_data = {'section': section}
#             students = []
#             for student in course.public_students.all():
#                 student_data = {'student': student}
#                 student_data['score'] = calculate_score(student, section)
#                 first_answer = UserAnswer.objects.filter(
#                     user=student, question__section=section).order_by(
#                     'test_was_taken').first()
#                 if first_answer is not None:
#                     student_data['test_was_taken'] = first_answer.test_was_taken
#                 students.append(student_data)
#             section_data['students'] = students
#             sections.append(section_data)
#         course_data['sections'] = sections
#         courses.append(course_data)
#     form = PublicSettingsForm(section_id, student)
#     section = Section.objects.get(id=section_id)
#     return render(request, 'courses/do_section.html', {
#         'student_data': student_data,
#         'form': form,
#         'section': section
# })


def do_test(request, section_id):
    if not request.user.is_authenticated():
        raise PermissionDenied
    user = request.user
    section = Section.objects.get(id=section_id)
    if section.has_taken_test(user):
        return redirect(reverse('student_detail'))
    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':  # problem was a typo 'csrfmiddletoken'
                continue
            # {'question-1': '2'}
            question_id = key.split('-')[1]
            answer_id = request.POST.get(key)
            data[question_id] = answer_id
        perform_test(request.user, data, section)
        return redirect(reverse('show_results', args=(section.id,)))
    return render(request, 'courses/do_test.html', {
        'section': section,
        'user': user
    })


def perform_test(user, data, section):
    with transaction.atomic():
        UserAnswer.objects.filter(user=user,
                                  question__section=section).delete()
        for question_id, answer_id in data.items():
            question = Question.objects.get(id=question_id)
            answer_id = int(answer_id)
            if answer_id not in question.answers.values_list('id', flat=True):
                raise SuspiciousOperation('Answer is not valid for this question')
            user_answer = UserAnswer.objects.create(
                user=user,
                question=question,
                answer_id=answer_id,
            )


def calculate_score(user, section):
    questions = Question.objects.filter(section=section)
    correct_answers = UserAnswer.objects.filter(
        user=user,
        question__section=section,
        answer__correct=True
    )
    return (correct_answers.count() / questions.count()) * 100


def show_results(request, section_id):
    if not request.user.is_authenticated():
        raise PermissionDenied
    section = Section.objects.get(id=section_id)
    #form = PublicComment.comment()
    #if request.method == 'POST':
    return render(request, 'courses/show_results.html', {
           # 'form': form,
        'section': section,
        'score': calculate_score(request.user, section)
    })


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    @detail_route(methods=['GET', ])
    def questions(self, request, *args, **kwargs):
        section = self.get_object()
        data = []
        for question in section.question_set.all():
            question_data = {'id': question.id, 'answers': []}
            for answer in question.answer_set.all():
                answer_data = {'id': answer.id, 'text': str(answer), }
                question_data['answers'].append(answer_data)
            data.append(question_data)
        return Response(data)

    @detail_route(methods=['PUT', ])
    def test(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied
        section = self.get_object()
        perform_test(request.user, request.data, section)
        return Response()

    @detail_route(methods=['GET'])
    def result(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied
        return Response({
            'score': calculate_score(request.user, self.get_object())
        })
