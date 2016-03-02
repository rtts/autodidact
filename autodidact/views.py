from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .utils import random_string
from .models import *

@login_required
def homepage(request):
    programmes = Programme.objects.all()
    return render(request, 'homepage.html', {
        'programmes': programmes,
    })

@login_required
def course(request, course):
    if request.user.is_staff:
        course = get_object_or_404(Course, slug=course)
    else:
        course = get_object_or_404(Course, slug=course, active=True)
    return render(request, 'course.html', {
        'course': course,
    })

@login_required
def session(request, course, session_nr):
    session_nr = int(session_nr)
    if request.user.is_staff:
        course = get_object_or_404(Course, slug=course)
    else:
        course = get_object_or_404(Course, slug=course, active=True)
    if session_nr < 1:
        raise Http404()
    try:
        session = course.sessions.all()[session_nr-1]
        session.nr = session_nr
    except IndexError:
        raise Http404()
    if not session.active and not request.user.is_staff:
        raise Http404()
    ticket_error  = False

    if session.registration_enabled and request.method == 'POST':
        ticket = request.POST.get('ticket')
        try:
            newclass = Class.objects.get(ticket=ticket)
            if newclass.session == session and not newclass.dismissed:
                newclass.users.add(request.user)
                return redirect(session)
            else:
                ticket_error = ticket
        except Class.DoesNotExist:
            ticket_error = ticket

    return render(request, 'session.html', {
        'course': course,
        'session': session,
        'ticket_error': ticket_error,
    })


@login_required
def assignment(request, course, session_nr, assignment_nr):
    session_nr    = int(session_nr)
    assignment_nr = int(assignment_nr)
    step_nr       = int(request.GET.get('step', 1))
    save_only     = request.GET.get('save_only', 'false')

    if request.user.is_staff:
        course = get_object_or_404(Course, slug=course)
    else:
        course = get_object_or_404(Course, slug=course, active=True)
    if session_nr < 1 or assignment_nr < 1:
        raise Http404()
    try:
        session = course.sessions.all()[session_nr-1]
        assignment = session.assignments.all()[assignment_nr-1]
    except IndexError:
        raise Http404()
    if not session.active and not request.user.is_staff:
        raise Http404()
    if not assignment.active and not request.user.is_staff:
        raise Http404()
    if assignment.locked and not request.user.is_staff:
        present = request.user.attends.all() & session.classes.all()
        if not present:
            return HttpResponseForbidden()

    # Retrieve current step
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
            CompletedStep(
                step=step,
                whom=request.user,
                answer=answer,
            ).save()

        # Redirect after POST request
        if direction == 'Previous':
            return redirect(reverse('assignment', args=[course.slug, session_nr, assignment_nr]) + "?step=" + str(step_nr - 1))
        elif direction == 'Next':
            return redirect(reverse('assignment', args=[course.slug, session_nr, assignment_nr]) + "?step=" + str(step_nr + 1))
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

    first = step == steps[0]
    last = step == steps[-1]
    count = len(steps)

    return render(request, 'assignment.html', {
        'course': course,
        'session': session,
        'session_nr': session_nr,
        'assignment': assignment,
        'assignment_nr': assignment_nr,
        'save_only': save_only == "true",
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
    unique = False

    # Generate unique registration code
    while not unique:
        ticket = random_string(TICKET_LENGTH)
        if not Class.objects.filter(ticket=ticket).exists():
            unique = True

    # Create a class and store it in the user's session
    newclass = Class(session=session, number=class_nr, ticket=ticket)
    newclass.save()
    request.session['current_class'] = newclass.ticket

    return redirect(session)

@staff_member_required
@require_http_methods(['POST'])
def endclass(request):
    session_pk = request.POST.get('session')
    session = get_object_or_404(Session, pk=session_pk)
    try:
        ticket = request.session['current_class']
        current_class = Class.objects.get(ticket=ticket)
        current_class.dismissed = True
        current_class.save()
        del request.session['current_class']
    except (KeyError, Class.DoesNotExist):
        pass
    return redirect(session)

# TODO: This method is currently unused
@staff_member_required
@require_http_methods(['POST'])
def joinclass(request):
    session_pk = request.POST.get('session')
    session = get_object_or_404(Session, pk=session_pk)
    ticket = request.POST.get('ticket')

    # Retrieve the class and store it in the user's session
    try:
        newclass = Class.objects.get(ticket=ticket)
        request.session['current_class'] = newclass.ticket
    except Class.DoesNotExist:
        pass

    return redirect(session)
