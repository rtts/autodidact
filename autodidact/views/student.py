import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from autodidact import gift
from autodidact.utils import *
from autodidact.models import *
from autodidact.views.decorators import *

@login_required
def user_settings(request):
    if request.POST:
        form = UserForm
    return render(request, 'autodidact/settings.html', {
    })

@login_required
def homepage(request):
    '''Serves the homepage'''

    if hasattr(request.user, 'uvt_user'):
        red = request.GET.get('redirect')
        if red != 'no' and request.user.uvt_user.programme:
            return redirect('programme', request.user.uvt_user.programme.slug)

    bachelor_programmes = Programme.objects.filter(degree=10)
    premaster_programmes = Programme.objects.filter(degree=20)
    master_programmes = Programme.objects.filter(degree=30)
    return render(request, 'autodidact/homepage.html', {
        'bachelor_programmes': bachelor_programmes,
        'premaster_programmes': premaster_programmes,
        'master_programmes': master_programmes,
    })

@login_required
def programme(request, slug):
    programme = get_object_or_404(Programme, slug=slug)
    if hasattr(request.user, 'uvt_user'):
        request.user.uvt_user.programme = programme
        request.user.uvt_user.save()
    return render(request, 'autodidact/programme.html', {
        'programme': programme,
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
    students = None

    calculate_progress(user, assignments)

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
                s.progress = calculate_progress(s, assignments)

    return render(request, 'autodidact/session_base.html', {
        'programme': programme,
        'course': course,
        'session': session,
        'assignments': assignments,
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
        step.given_values = request.POST.getlist('answer')
        concatenated_values = '\x1e'.join(step.given_values)
        if step.completedstep:
            step.completedstep.answer = concatenated_values
        else:
            step.completedstep = CompletedStep(step=step, whom=request.user, answer=concatenated_values)
        if step.graded:
            if step.multiple_choice and step.multiple_answers:
                step.completedstep.passed = gift.all_correct(step.given_values, step.right_values)
            else:
                step.completedstep.passed = gift.any_correct(step.given_values, step.right_values)
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
