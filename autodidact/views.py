from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .decorators import *
from .utils import *
from .models import *

@login_required
def homepage(request):
    programmes = Programme.objects.all()
    return render(request, 'homepage.html', {
        'programmes': programmes,
    })

@login_required
@needs_course
def course(request, course):
    return render(request, 'course.html', {
        'course': course,
    })

@login_required
@needs_course
@needs_session
def session(request, course, session):
    current_class = None
    ticket_error = False
    assignments = session.assignments.prefetch_related('steps')
    (answers, progress) = calculate_progress(request.user, assignments)
    students = None

    if session.registration_enabled:
        if request.method == 'POST':
            ticket = request.POST.get('ticket')
            try:
                newclass = Class.objects.get(ticket=ticket)
            except Class.DoesNotExist:
                newclass = None
            if newclass and newclass.session == session and not newclass.dismissed:
                newclass.students.add(request.user)
                return redirect(session)
            else:
                ticket_error = ticket

        current_class = get_current_class(session, request)
        if request.user.is_staff and current_class:
            students = current_class.students.all()
            for student in students:
                (answers, progress) = calculate_progress(student, assignments)
                student.progress = progress
                student.answers = answers

    return render(request, 'session.html', {
        'course': course,
        'session': session,
        'answers': answers,
        'progress': progress,
        'students': students,
        'current_class': current_class,
        'ticket_error': ticket_error,
    })

def get_current_class(session, request):
    user = request.user
    if user.is_staff:
        classes = user.teaches.all() & session.classes.all()
    else:
        classes = user.attends.all() & session.classes.all()
    return classes[0] if classes else None

def calculate_progress(student, assignments):
    answers   = []
    progress  = []
    completed = student.completed.select_related('step').order_by('step')

    for ass in assignments:
        step_count = 0
        completed_count = 0
        answers.append([])
        progress.append(None)
        if not ass.active:
            continue
        for step in ass.steps.all():
            step_count += 1
            answers[-1].append('')
            for com in completed:
                if step == com.step:
                    completed_count += 1
                    if step.answer_required and not com.answer:
                        answers[-1][-1] = "mispoes"
                    else:
                        answers[-1][-1] = com.answer
                    break
        if step_count:
            progress[-1] = 100 * completed_count/step_count
        else:
            progress[-1] = 0

    return (answers, progress)

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

    return render(request, 'assignment.html', {
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
