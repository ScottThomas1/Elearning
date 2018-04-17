from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from students.models import User
from courses.models import Course, UserAnswer, Answer
from courses.views import calculate_score


def get_all_scores_for_user(user):
    scores = []
    for course in Course.objects.filter(students=user):  # gets the course the user is in
        course_data = {'course': course}                 # dict to call the course later
        sections = []                                    # list for sections
        for section in course.section_set.order_by('number'):   # ordering by the section inside the course
            section_data = {'score': calculate_score(user, section), 'section': section} # dict to get user score for sec
            questions = []                               # creates a list called questions
            for question in section.questions.all():     # for every question in each section get all
                question_data = {'correct_answer': question.answers.filter(correct=True), 'question': question}
                try:  # line 18 is a dict with correct_answer
                    useranswer = question.useranswers.get(user=user)  #
                except UserAnswer.DoesNotExist:
                    useranswer = None
                if useranswer is not None and useranswer.answer in question_data['correct_answer']:
                    question_data['correct'] = True
                else:
                    question_data['correct'] = False
                question_data['useranswer'] = useranswer
                questions.append(question_data)
            section_data['questions'] = questions
            sections.append(section_data)
        course_data['sections'] = sections
        scores.append(course_data)
    return scores


def student_detail(request):
    if not request.user.is_authenticated():
        raise PermissionDenied
    student = request.user
    #useranswers = UserAnswer.objects.all()
    #answer = UserAnswer.objects.filter(answer__correct=True, user=student, question__section__course_id=13)
    return render(request, 'students/student_detail.html', {
        #'answer': answer,
        #'useranswers': useranswers,
        'student': student,
        'scores': get_all_scores_for_user(student),
    })
