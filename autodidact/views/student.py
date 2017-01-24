import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from autodidact import gift
from autodidact.decorators import *
from autodidact.utils import *
from autodidact.models import *

@login_required
def page(request, slug=''):
    '''Serves a particular page. Mainly used for serving the homepage.
    '''
    page = get_object_or_404(Page, slug=slug)
    programmes = Programme.objects.all()
    return render(request, 'autodidact/page.html', {
        'page': page,
        'programmes': programmes,
    })

@login_required
@needs_course
def course(request, course):
    '''Serves the course overview page
    '''
    return render(request, 'autodidact/course.html', {
        'course': course,
    })

@login_required
@needs_course
def topic(request, course, topic_nr):
    '''Serves a topic page that belong to a course
    '''
    topic = get_object_or_404(Topic, course=course, number=topic_nr)
    return render(request, 'autodidact/topic.html', {
        'topic': topic,
        'course': course,
    })

@login_required
@needs_course
@needs_session
def session(request, course, session):
    '''Serves the session overview page
    '''
    user = request.user
    current_class = None
    ticket_error = False
    assignments = session.assignments.prefetch_related('steps')
    (answers, progress) = calculate_progress(user, assignments)
    students = None

    if session.registration_enabled:
        if request.method == 'POST':
            ticket = request.POST.get('ticket')
            try:
                newclass = Class.objects.get(ticket=ticket, dismissed=False)
            except Class.DoesNotExist:
                newclass = None
            if newclass and newclass.session == session:
                newclass.students.add(user)
                return redirect(session)
            else:
                ticket_error = ticket

        current_class = get_current_class(session, user)
        if user.is_staff and current_class:
            students = current_class.students.all()
            for s in students:
                (answers, progress) = calculate_progress(s, assignments)
                s.progress = progress
                s.answers = answers

    return render(request, 'autodidact/session_base.html', {
        'course': course,
        'session': session,
        'assignments': assignments,
        'answers': answers,
        'progress': progress,
        'students': students,
        'current_class': current_class,
        'ticket_error': ticket_error,
    })

@login_required
@needs_course
@needs_session
@needs_assignment
@needs_step
def assignment(request, course, session, assignment, step):
    '''This view shows the current step of an assignment. Submitted
    answers will always be saved and, if needed, checked for
    correctness.

    '''
    if request.method == 'POST':
        given_values = request.POST.getlist('answer')
        concatenated_values = '\x1e'.join(given_values)
        if step.completedstep:
            step.completedstep.answer = concatenated_values
        else:
            step.completedstep = CompletedStep(step=step, whom=request.user, answer=concatenated_values)
        if step.graded:
            if step.multiple_choice and step.multiple_answers:
                step.completedstep.passed = gift.all_correct(given_values, step.right_values)
            else:
                step.completedstep.passed = gift.any_correct(given_values, step.right_values)
        else:
            step.completedstep.passed = True
        step.completedstep.save()

        if 'previous' in request.POST:
            new_step = assignment.steps.filter(number__lt=step.number).last()
        elif 'step' in request.POST:
            new_step = assignment.steps.filter(number=request.POST['step']).first()
        elif 'next' in request.POST:
            new_step = assignment.steps.filter(number__gt=step.number).first()
        else:
            new_step = None

        if 'next' in request.POST and not step.completedstep.passed:
            step.please_try_again = True
        elif new_step:
            new_step.fullscreen = step.fullscreen
            return redirect(new_step)
        else:
            return redirect(session)

    steps = list(assignment.steps.all())
    answered_steps = [c.step for c in request.user.completed.filter(passed=True, step__assignment=assignment).select_related('step')]
    for s in steps:
        s.passed = s in answered_steps
    step.is_first = step == steps[0]
    step.is_last = step == steps[-1]
    step.answers = step.right_values + step.wrong_values
    random.shuffle(step.answers)
    try:
        # Move these answers to the front if they exist
        for val in ['Yes', 'yes', 'True', 'true']:
            step.answers.remove(val)
            step.answers.insert(0, val)
    except ValueError:
        pass

    template = 'autodidact/assignment_fullscreen.html' if step.fullscreen else 'autodidact/assignment.html'
    return render(request, template, {
        'course': course,
        'session': session,
        'assignment': assignment,
        'step': step,
        'steps': steps,
    })
