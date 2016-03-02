from django import template
from ..models import *

register = template.Library()

@register.inclusion_tag('autodidact/nav_homepage.html', takes_context=True)
def autodidact_navigation(context, programmes):
    user = context['user']
    return {
        'user': user,
        'programmes': programmes,
    }

@register.inclusion_tag('autodidact/nav_course.html', takes_context=True)
def autodidact_course_navigation(context, course):
    user = context['user']
    return {
        'user': user,
        'course': course,
    }

@register.inclusion_tag('autodidact/nav_session.html', takes_context=True)
def autodidact_session_navigation(context, session):
    request = context['request']
    user = context['user']
    course = session.course
    current_class = get_current_class(session, request)
    return {
        'user': user,
        'course': course,
        'session': session,
        'current_class': current_class,
    }

@register.inclusion_tag('autodidact/nav_assignment.html', takes_context=True)
def autodidact_assignment_navigation(context, assignment):
    user = context['user']
    session = assignment.session
    course = assignment.session.course
    return {
        'user': user,
        'course': course,
        'session': session,
        'assignment': assignment,
    }

@register.inclusion_tag('autodidact/editor.html', takes_context=True)
def autodidact_editor(context):
    context['edit_type'] = context['request'].resolver_match.view_name
    return context

@register.inclusion_tag('autodidact/registration.html', takes_context=True)
def autodidact_registration(context, session):
    request = context['request']
    user = context['user']
    current_class = get_current_class(session, request)
    return {
        'user': user,
        'session': session,
        'current_class': current_class,
        'ticket_error': context['ticket_error'],
    }

@register.inclusion_tag('autodidact/progress.html', takes_context=True)
def autodidact_progress(context, session):
    request = context['request']
    user = context['user']
    current_class = get_current_class(session, request)
    assignments = session.assignments.prefetch_related('steps')
    (answers, progress) = calculate_progress(request.user, assignments)
    students = None

    if session.registration_enabled and user.is_staff and current_class:
        students = current_class.users.all()
        for student in students:
            (answers, progress) = calculate_progress(student, assignments)
            student.progress = progress
            student.answers = answers

    return {
        'user': user,
        'session': session,
        'current_class': current_class,
        'assignments': assignments,
        'answers': answers,
        'progress': progress,
        'students': students,
    }

def get_current_class(session, request):
    user = request.user
    present = user.attends.all() & session.classes.all()
    if user.is_staff:
        try:
            current_class = Class.objects.get(
                ticket = request.session['current_class'],
                session = session,
            )
            present = [ current_class ]
        except (Class.DoesNotExist, KeyError):
            pass
    return present[0] if present else None

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
