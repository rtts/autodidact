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
    students = None
    present = False
    current_class = None

    if session_nr < 1:
        raise Http404()
    try:
        session = course.sessions.all()[session_nr-1]
        session.nr = session_nr
    except IndexError:
        raise Http404()
    if not session.active and not request.user.is_staff:
        raise Http404()

    assignments = session.assignments.select_related('steps')
    completed = request.user.completed.select_related('step').order_by('step')

    if session.registration_enabled:
        if request.method == 'POST':
            ticket = request.POST.get('ticket')
            try:
                newclass = Class.objects.get(ticket=ticket)
                if newclass.session == session:
                    newclass.users.add(request.user)
            except Class.DoesNotExist:
                pass
            return redirect(session)

        # Users are present if their classes intersect the session's classes
        present = request.user.attends.all() & session.classes.all()

        try:
            current_class = Class.objects.get(ticket=request.session['current_class'], session=session)
        except (Class.DoesNotExist, KeyError):
            pass

        # For teachers, calculate the progress of each student
        if request.user.is_staff and current_class:
            students = current_class.users.select_related('completed', 'completed__step')
            for student in students:
                completed_by_student = student.completed.order_by('step')
                student.progress = []
                for i, ass in enumerate(assignments):
                    step_count = 0
                    completed_count = 0
                    ass.nr = i + 1
                    for step in ass.steps.all():
                        step_count += 1
                        for com in completed_by_student:
                            if step == com.step:
                                completed_count += 1
                                break
                    if step_count:
                        percentage_completed = 100 * completed_count/step_count
                    else:
                        percentage_completed = 0
                    student.progress.append(percentage_completed)

    # Calculate answers, progress, and assignment lists
    answers = []
    preliminary_assignments = []
    inclass_assignments = []
    for i, ass in enumerate(assignments):
        step_count = 0
        completed_count = 0
        ass.nr = i + 1
        answers.append([])
        if ass.type == 1:
            preliminary_assignments.append(ass)
        elif ass.type == 2:
            inclass_assignments.append(ass)
        for step in ass.steps.all():
            step_count += 1
            answers[i].append('')
            for com in completed:
                if step == com.step:
                    completed_count += 1
                    if step.answer_required and not com.answer:
                        answers[i][-1] = "mispoes"
                    else:
                        answers[i][-1] = com.answer
                    break
        if step_count:
            percentage_completed = 100 * completed_count/step_count
        else:
            percentage_completed = 0
        ass.percentage = percentage_completed

    return render(request, 'session.html', {
        'course': course,
        'session': session,
        'assignments': assignments,
        'preliminary_assignments': preliminary_assignments,
        'inclass_assignments': inclass_assignments,
        'answers': answers,
        'present': present,
        'current_class': current_class,
        'students': students,
    })

@login_required
def assignment(request, course, session_nr, assignment_nr):
    session_nr = int(session_nr)
    assignment_nr = int(assignment_nr)
    step_nr = int(request.GET.get('step', 1))
    save_only = request.GET.get('save_only', 'false')
    if request.user.is_staff:
        course = get_object_or_404(Course, slug=course)
    else:
        course = get_object_or_404(Course, slug=course, active=True)

    # Retrieve session and assignment objects
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

    # Locked assignments can only be made by in-class users (and staff)
    if assignment.locked:
        present = request.user.attends.all() & session.classes.all()
        if not present and not request.user.is_staff:
            return HttpResponseForbidden()

    # Retrieve current step and whether it's completed
    if step_nr < 1:
        return redirect(assignment)
    try:
        step = assignment.steps.all()[step_nr-1]
        completed = CompletedStep.objects.get(
            whom=request.user,
            step=step,
        )
    except IndexError:
        step = False
        completed = False
    except CompletedStep.DoesNotExist:
        completed = False

    if request.method == 'POST' and step:
        direction = request.POST.get('direction', '')
        answer = request.POST.get('answer', '')

        # Save state after each step
        if completed:
            completed.answer = answer
            completed.save()
        else:
            CompletedStep(
                step=step,
                whom=request.user,
                answer=answer,
            ).save()

        # Redirect after POST request
        if direction in ['Save', 'Finish!']:
            return redirect(session)
        elif direction == 'Previous':
            return redirect(reverse('assignment', args=[course.slug, session_nr, assignment_nr]) + "?step=" + str(step_nr - 1))
        elif direction == 'Next':
            return redirect(reverse('assignment', args=[course.slug, session_nr, assignment_nr]) + "?step=" + str(step_nr + 1))

    first = step == assignment.steps.first()
    last = step == assignment.steps.last()
    count = assignment.steps.count()

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
        'completed': completed,
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
        del request.session['current_class']
    except KeyError:
        pass
    return redirect(session)

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
