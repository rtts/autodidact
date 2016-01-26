from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from autodidact.models import *

@login_required
def homepage(request):
    programmes = Programme.objects.all()
    return render(request, 'homepage.html', {
        'programmes': programmes,
    })

@login_required
def course(request, course):
    course = get_object_or_404(Course, slug=course)
    return render(request, 'course.html', {
        'course': course,
    })

@login_required
def session(request, course, session_nr):
    session_nr = int(session_nr)
    course = get_object_or_404(Course, slug=course)
    session = course.sessions.all()[session_nr-1]

    # TODO: Perform the following in a single, efficient database query
    assignments = session.assignments.select_related('activities')
    completed = request.user.completed.select_related('activity').order_by('activity')
    answers = []
    percentages = []
    for i, ass in enumerate(assignments):
        answers.append([])
        activities_count = 0
        completed_count = 0
        for step in ass.activities.all():
            activities_count += 1
            answers[i].append('')
            for com in completed:
                if step == com.activity:
                    completed_count += 1
                    if step.answer_required and not com.answer:
                        answers[i][-1] = "mispoes"
                    else:
                        answers[i][-1] = com.answer
                    break
        if activities_count:
            percentage_completed = 100 * completed_count/activities_count
        else:
            percentage_completed = 0
        percentages.append(percentage_completed)

    return render(request, 'session.html', {
        'course': course,
        'session': session,
        'session_nr': session_nr,
        'answers': answers,
        'percentages': percentages,
    })

@login_required
def assignment(request, course, session_nr, assignment_nr):
    session_nr = int(session_nr)
    assignment_nr = int(assignment_nr)
    activity_nr = int(request.GET.get('step', 1))
    save_only = request.GET.get('save_only', 'false')
    course = get_object_or_404(Course, slug=course)
    session = course.sessions.all()[session_nr-1]
    assignment = session.assignments.all()[assignment_nr-1]
    count = assignment.activities.count()

    # Carefully extract the current activity and whether it's completed
    if activity_nr < 1:
        return redirect(assignment)
    try:
        activity = assignment.activities.all()[activity_nr-1]
        completed = CompletedActivity.objects.get(
            whom=request.user,
            activity=activity,
        )
    except IndexError:
        activity = False
        completed = False
    except CompletedActivity.DoesNotExist:
        completed = False

    if request.method == 'POST' and activity:
        direction = request.POST.get('direction', '')
        answer = request.POST.get('answer', '')

        # Save state when the user advances
        if direction in ['Next', 'Save', 'Finish!']:
            if completed:
                completed.answer = answer
                completed.save()
            else:
                CompletedActivity(
                    activity=activity,
                    whom=request.user,
                    answer=answer,
                ).save()

        # Redirect after POST request
        if direction in ['Save', 'Finish!']:
            return redirect(session)
        elif direction == 'Previous':
            return redirect(reverse('assignment', args=[course.slug, session_nr, assignment_nr]) + "?step=" + str(activity_nr - 1))
        elif direction == 'Next':
            return redirect(reverse('assignment', args=[course.slug, session_nr, assignment_nr]) + "?step=" + str(activity_nr + 1))

    first = activity == assignment.activities.first()
    last = activity == assignment.activities.last()

    return render(request, 'assignment.html', {
        'course': course,
        'session': session,
        'session_nr': session_nr,
        'assignment': assignment,
        'assignment_nr': assignment_nr,
        'save_only': save_only == "true",
        'activity': activity,
        'activity_nr': activity_nr,
        'count': count,
        'completed': completed,
        'first': first,
        'last': last,
    })
