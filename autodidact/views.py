from datetime import datetime, timedelta
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .decorators import *
from .utils import *
from .models import *

@login_required
def homepage(request):
    programmes = Programme.objects.all()
    return render(request, 'autodidact/homepage.html', {
        'programmes': programmes,
    })

@login_required
@needs_course
def course(request, course):
    return render(request, 'autodidact/course.html', {
        'course': course,
    })

@login_required
@needs_course
@needs_session
def session(request, course, session):
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
                newclass = Class.objects.get(ticket=ticket)
            except Class.DoesNotExist:
                newclass = None
            if newclass and newclass.session == session and not newclass.dismissed:
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

@staff_member_required
@needs_course
@needs_session
def progress(request, course, session, username):
    try:
        student = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise Http404
    assignments = session.assignments.prefetch_related('steps')
    (answers, progress) = calculate_progress(student, assignments)
    current_class = get_current_class(session, request.user)
    return render(request, 'autodidact/session_progress.html', {
        'course': course,
        'session': session,
        'assignments': assignments,
        'answers': answers,
        'progress': progress,
        'student': student,
        'current_class': current_class,
    })

@staff_member_required
@needs_course
@needs_session
def progresses(request, course, session):
    try:
        days = int(request.GET['days'])
    except (ValueError, KeyError):
        return HttpResponseBadRequest('Days not specified')
    if days < 0 or days > 365000:
        return HttpResponseBadRequest('Invalid number of days')
    filetype = request.GET.get('filetype')
    assignments = session.assignments.prefetch_related('steps')
    current_class = get_current_class(session, request.user)
    enddate = datetime.today() + timedelta(days=1)
    startdate = enddate - timedelta(days=days+1)
    classes = Class.objects.filter(session=session, date__range=[startdate, enddate]).prefetch_related('students')
    students = get_user_model().objects.filter(attends__in=classes).distinct()
    for s in students:
        (answers, progress) = calculate_progress(s, assignments)
        s.progress = progress
        s.answers = answers

    if filetype == 'csv':
        response = render(request, 'autodidact/students.csv', {'students': students})
        response['Content-Disposition'] = 'attachment; filename="{}_session{}.csv"'.format(course.slug, session.nr)
        return response
    else:
        return render(request, 'autodidact/session_progresses.html', {
        'days': days,
        'course': course,
        'session': session,
        'assignments': assignments,
        'students': students,
        'current_class': current_class,
    })

@login_required
@needs_course
@needs_session
@needs_assignment
def assignment(request, course, session, assignment):
    step_nr = int(request.GET.get('step', 1))
    steps = list(assignment.steps.all())
    if step_nr < 1:
        return redirect(assignment)
    try:
        step = steps[step_nr-1]
    except IndexError:
        step = None

    # Retrieve answer of current step
    current_answer = None
    all_answers = request.user.completed.filter(step__assignment=assignment).select_related('step')
    for ans in all_answers:
        if step == ans.step:
            current_answer = ans
            break

    if request.method == 'POST' and step:
        direction = request.POST.get('direction', '')
        answer = request.POST.get('answer', '')

        # Save state after each step
        if current_answer:
            current_answer.answer = answer
            current_answer.save()
        else:
            CompletedStep(step=step, whom=request.user, answer=answer).save()

        # Redirect after POST request
        if direction == 'Previous':
            return redirect(reverse('assignment', args=[course.slug, session.nr, assignment.nr]) + "?step=" + str(step_nr - 1))
        elif direction == 'Next':
            return redirect(reverse('assignment', args=[course.slug, session.nr, assignment.nr]) + "?step=" + str(step_nr + 1))
        else:
            return redirect(session)

    # Calculate for all steps whether they have answers
    step_overview = []
    answered_steps = [ans.step for ans in all_answers]
    for s in steps:
        if s in answered_steps:
            step_overview.append(True)
        else:
            step_overview.append(False)

    # BUG: IndexError when step is None
    first = step == steps[0]
    last = step == steps[-1]
    count = len(steps)

    return render(request, 'autodidact/assignment.html', {
        'course': course,
        'session': session,
        'assignment': assignment,
        'step': step,
        'step_nr': step_nr,
        'count': count,
        'completed': current_answer,
        'step_overview': step_overview,
        'first': first,
        'last': last,
    })

@staff_member_required
@require_http_methods(['POST'])
def startclass(request):
    session_pk = request.POST.get('session')
    class_nr = request.POST.get('class_nr')
    if len(class_nr) > 16:
        return HttpResponseBadRequest()
    session = get_object_or_404(Session, pk=session_pk)

    # Generate unique registration code
    unique = False
    while not unique:
        ticket = random_string(TICKET_LENGTH)
        if not Class.objects.filter(ticket=ticket).exists():
            unique = True

    Class(session=session, number=class_nr, ticket=ticket, teacher=request.user).save()
    return redirect(session)

@staff_member_required
@require_http_methods(['POST'])
def endclass(request):
    class_pk = request.POST.get('class')
    session_pk = request.POST.get('session')
    session = get_object_or_404(Session, pk=session_pk)
    try:
        group = Class.objects.get(pk=class_pk)
        group.teacher = None
        group.dismissed = True
        group.save()
    except Class.DoesNotExist:
        pass
    return redirect(session)
