import xlsxwriter
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required

from autodidact.utils import *
from autodidact.models import *
from autodidact.views.decorators import *

@staff_member_required
def documentation(request, slug=''):
    '''Serves a documentation page.
    '''
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'autodidact/page.html', {
        'page': page,
    })

@staff_member_required
@needs_course
@needs_session
def print_session(request, course, session):
    assignments = session.assignments.filter(active=True).prefetch_related('steps')
    return render(request, 'autodidact/print_session.html', {
        'course': course,
        'session': session,
        'assignments': assignments,
    })

@staff_member_required
@needs_course
@needs_session
def progresses(request, course, session):
    '''This view renders a table with all the students that participated
    in a given session during a given time period. If the filetype
    'csv' or 'xlsx' is specified, it exports the list of names in that
    format.

    '''
    try:
        days = int(request.GET['days'])
    except (ValueError, KeyError):
        return HttpResponseBadRequest('Days not specified')
    if days < 0 or days > 365000:
        return HttpResponseBadRequest('Invalid number of days')
    filetype = request.GET.get('filetype')
    assignments = session.assignments.prefetch_related('steps')
    current_class = get_current_class(session, request.user)

    # End date is today 23:59:59
    enddate = timezone.now().replace(hour=23, minute=59, second=59, microsecond=0)

    # Start date is $days earlier, 00:00:00
    startdate = (enddate - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)

    classes = Class.objects.filter(session=session, date__range=[startdate, enddate]).prefetch_related('students')
    students = get_user_model().objects.filter(attends__in=classes).order_by('last_name').distinct().select_related('uvt_user')
    for s in students:
        s.progress = calculate_progress(s, assignments)

    if filetype == 'xlsx':
        try:
            # Python 2
            from StringIO import StringIO
        except ImportError:
            # Python 3
            from io import BytesIO as StringIO

        file = StringIO()
        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 0, 24)
        default = workbook.add_format({'border': 1})
        bold = workbook.add_format({'bold': True, 'border': 1})
        worksheet.write(0, 0, 'Name', bold)
        worksheet.write(0, 1, 'emplId', bold)
        for row, student in enumerate(students, start=1):
            if hasattr(student, 'uvt_user'):
                worksheet.write(row, 0, student.uvt_user.full_name, default)
                if student.uvt_user.emplId:
                    worksheet.write(row, 1, student.uvt_user.emplId, default)
                else:
                    worksheet.write(row, 1, 'n/a', default)
            else:
                worksheet.write(row, 0, student.get_full_name(), default)
                worksheet.write(row, 1, 'n/a', default)
        workbook.close()

        response = HttpResponse(file.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="{} Session {} attendees from {} to {}.xlsx"'.format(course.colloquial_name(), session.number, startdate.strftime("%Y-%m-%d"), enddate.strftime("%Y-%m-%d"))
        file.close()
        return response

    return render(request, 'autodidact/session_progresses.html', {
        'days': days,
        'course': course,
        'session': session,
        'assignments': assignments,
        'students': students,
        'current_class': current_class,
    })

@staff_member_required
@needs_course
@needs_session
def progress(request, course, session, username):
    '''This view shows a staff member the progress of a specific student

    '''
    try:
        student = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise Http404
    assignments = session.assignments.prefetch_related('steps')
    progress = calculate_progress(student, assignments)
    current_class = get_current_class(session, request.user)
    student_attends = (student.attends.all() & session.classes.all()).first()
    return render(request, 'autodidact/session_progress.html', {
        'course': course,
        'session': session,
        'assignments': assignments,
        'progress': progress,
        'student': student,
        'current_class': current_class,
        'student_attends': student_attends,
    })

@staff_member_required
@needs_course
@needs_session
@require_http_methods(['POST'])
def add_student(request, course, session):
    '''A simple form endpoint to manually add a student to a class

    '''
    try:
        username = request.POST['username']
        student = get_user_model().objects.get(username=username)
        klass = get_current_class(session, request.user)
        klass.students.add(student)
    except (AttributeError, KeyError, get_user_model().DoesNotExist):
        pass
    return redirect('session', course.slug, session.number)

@staff_member_required
@needs_course
@needs_session
def remove_student(request, course, session, username):
    '''A simple form endpoint to manually remove a student from a class

    '''
    try:
        student = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise Http404
    classes = student.attends.filter(session=session)
    for klass in classes:
        klass.students.remove(student)
    return redirect('session', course.slug, session.number)

@staff_member_required
@require_http_methods(['POST'])
def startclass(request):
    '''This views starts a new class. The staff member that clicks the
    "Start a new class" button automatically becomes the teacher of
    the class.

    '''
    session_pk = request.POST.get('session')
    class_nr = request.POST.get('class_nr')
    if len(class_nr) > 16:
        return HttpResponseBadRequest()
    if class_nr == '':
        class_nr = 'nameless'
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
    '''This view ends a class by setting its attribute "dismissed" to true

    '''
    class_pk = request.POST.get('class')
    session_pk = request.POST.get('session')
    session = get_object_or_404(Session, pk=session_pk)
    try:
        group = Class.objects.get(pk=class_pk)
        group.dismissed = True
        group.save()
    except Class.DoesNotExist:
        pass
    return redirect(session)

@staff_member_required
@permission_required(['autodidact.add_session'])
@needs_course
def add_session(request, course):
    '''This allows teachers to add new sessions, without being bothered
    to choose a course when using the regular admin:add view

    '''
    session = Session(course=course, active=False)
    session.save()
    return redirect(session)

@staff_member_required
@permission_required(['autodidact.add_assignment'])
@needs_course
@needs_session
def add_assignment(request, course, session):
    '''This allows teachers to add new assignments, without being bothered
    to choose a session when using the regular admin:add view

    '''
    assignment = Assignment(session=session)
    assignment.save()
    return redirect(assignment)

@staff_member_required
@permission_required(['autodidact.add_assignment'])
@needs_course
@needs_session
@needs_assignment
def copy_assignment(request, course, session, assignment):
    '''Duplicates an assignment

    '''
    [assignment] = duplicate_assignment(None, None, [assignment])
    return HttpResponseRedirect(reverse('admin:autodidact_assignment_change', args=[assignment.pk]))

@staff_member_required
@permission_required(['autodidact.add_session'])
@needs_course
@needs_session
def copy_session(request, course, session):
    '''Duplicates a session

    '''
    [session] = duplicate_session(None, None, [session])
    return HttpResponseRedirect(reverse('admin:autodidact_session_change', args=[session.pk]))

@staff_member_required
@permission_required(['autodidact.add_course'])
@needs_course
def copy_course(request, course):
    '''Duplicates a course

    '''
    [course] = duplicate_course(None, None, [course])
    return HttpResponseRedirect(reverse('admin:autodidact_course_change', args=[course.pk]))

@staff_member_required
@permission_required(['autodidact.add_step', 'autodidact.change_step'])
@needs_course
@needs_session
@needs_assignment
def add_step(request, course, session, assignment):
    '''This allows teachers to add new steps, without being bothered
    to choose a assignment when using the regular admin:add view

    '''
    step = Step(assignment=assignment)
    step.save()
    return HttpResponseRedirect(reverse('admin:autodidact_step_change', args=[step.pk]))

@staff_member_required
@permission_required(['autodidact.delete_step', 'autodidact.change_step'])
@needs_course
@needs_session
@needs_assignment
@needs_step
def delete_step(request, course, session, assignment, step):
    '''Delete a step and reorders the remaining ones

    '''
    step.delete()
    try:
        assignment.steps.first().save()
    except AttributeError:
        pass

    return HttpResponseRedirect(reverse('assignment', args=[course.slug, session.number, assignment.number]))
