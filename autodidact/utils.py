from __future__ import unicode_literals
import sys
import random
import string
import unicodedata
from django.utils import timezone
from django.core.files.base import ContentFile

HUMAN_FRIENDLY_CHARS = '234679ABCDEFGHJKLMNPRSTUVWXYZabcdefghijkmnpqrstuvwxyz'

def get_current_class(session, user):
    '''For teachers, returns the class they are teaching. For students,
    returns the class they are registered for. Returns none otherwise.

    '''
    if user.is_staff:
        classes = user.teaches.filter(dismissed=False) & session.classes.all()
    else:
        classes = user.attends.all() & session.classes.all()
    return classes[0] if classes else None

def calculate_progress(user, assignments):
    '''Calculate and returns a list of percentages, indicating the user's
    progress in the corresponding assignment. As a side effect, it
    adds a 'progress' attribute to assignment objects and a
    'completedstep' attribute to step objects.

    '''
    progresses = []
    completed = user.completed.select_related('step')

    for ass in assignments:
        if not ass.active:
            continue
        step_count = 0
        completed_count = 0
        for step in ass.steps.all():
            step_count += 1
            for com in completed:
                if step == com.step:
                    if com.passed:
                        completed_count += 1
                    step.completedstep = com
                    step.given_values = com.answer.split('\x1e')
                    break
        ass.progress = int(100 * completed_count/step_count) if step_count else 0
        progresses.append(ass.progress)

    return progresses

def duplicate_assignment(modeladmin, request, queryset, rename=True):
    '''Duplicates an assignment including all underlying steps. Can be used as an admin action.'''

    duplicated_assignments = []
    for assignment in queryset:
        steps = assignment.steps.all()
        assignment.pk = None
        if rename:
            assignment.active = False
            assignment.name = (assignment.name + ' (duplicate)').lstrip()
        assignment.number = None
        assignment.save()
        assignment.steps.first().delete() # this deletes the automatically generated empty step

        for step in steps:
            right_answers = step.right_answers.all()
            wrong_answers = step.wrong_answers.all()
            clarifications = step.clarifications.all()
            stepfiles = step.files.all()

            # The following Just Works™ because id(assignment) == id(step.assignment)
            step.pk = None
            step.save()

            for right_answer in right_answers:
                right_answer.pk = None
                right_answer.save()

            for wrong_answer in wrong_answers:
                wrong_answer.pk = None
                wrong_answer.save()

            for clarification in clarifications:
                clarification.pk = None
                try:
                    clarification.image.save(clarification.image.name, ContentFile(clarification.image.read()))
                except:
                    pass
                clarification.save()

            for stepfile in stepfiles:
                stepfile.pk = None
                try:
                    stepfile.file.save(stepfile.file.name, ContentFile(stepfile.file.read()))
                except:
                    pass

        duplicated_assignments.append(assignment)
    return duplicated_assignments
duplicate_assignment.short_description = 'Duplicate the selected assignments'

def duplicate_session(modeladmin, request, queryset, rename=True):
    '''Duplicates a session, including all assignments'''

    duplicated_sessions = []
    for session in queryset:
        assignments = session.assignments.all()
        downloads = session.downloads.all()
        presentations = session.presentations.all()

        session.pk = None
        if rename:
            session.active = False
            session.name = session.name + ' (duplicate)'
        session.number = None
        session.save()

        for assignment in assignments:
            [assignment] = duplicate_assignment(None, None, [assignment], rename=False)
            assignment.session = session
            assignment.save()

        for download in downloads:
            download.pk = None
            try:
                download.file.save(download.file.name, ContentFile(download.file.read()))
            except:
                pass

        for presentation in presentations:
            presentation.pk = None
            try:
                presentation.file.save(presentation.file.name, ContentFile(presentation.file.read()))
            except:
                pass

        duplicated_sessions.append(session)
    return duplicated_sessions
duplicate_session.short_description = 'Duplicate the selected sessions'

def duplicate_course(modeladmin, request, queryset):
    '''Duplicates an entire course'''

    # deferred import to prevent circularity
    from .models import Course

    duplicated_courses = []
    for course in queryset:
        sessions = course.sessions.all()
        topics = course.topics.all()
        course.pk = None
        course.order = None
        course.active = False

        year = str(timezone.now().year)
        original_slug = course.slug
        course.name = (course.name + ' ' + year)
        course.slug = (original_slug + year)
        i = 1
        while Course.objects.filter(slug=course.slug).exists():
            course.slug = (original_slug + year + string.ascii_lowercase[i])
            i += 1
            if i > 25:
                course.slug = (original_slug + year + random_string(5))
        course.save()

        for session in sessions:
            [session] = duplicate_session(None, None, [session], rename=False)
            session.course = course
            session.save()

        for topic in topics:
            topic.pk = None
            topic.save()

        duplicated_courses.append(course)
    return duplicated_courses
duplicate_course.short_description = 'Duplicate the selected courses'

def random_string(length):
    '''Generates a random string of human friendly characters

    '''
    return ''.join(random.choice(HUMAN_FRIENDLY_CHARS) for x in range(length))

def clean(dirty_filename):
    '''Cleans dirty filenames

    '''
    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)

    # Replace accented characters with unaccented ones
    normalized_filename = unicodedata.normalize('NFKD', dirty_filename)

    # Strip out all characters that are not in @valid_chars
    cleaned_filename = ''.join([c for c in normalized_filename if c in valid_chars])

    return cleaned_filename
