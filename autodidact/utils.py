from __future__ import unicode_literals
import sys
import random
import string
import unicodedata

HUMAN_FRIENDLY_CHARS = '234679ABCDEFGHJKLMNPRSTUVWXYZabcdefghijkmnpqrstuvwxyz'

def get_current_class(session, user):
    if user.is_staff:
        classes = user.teaches.filter(dismissed=False) & session.classes.all()
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
            progress[-1] = int(100 * completed_count/step_count)
        else:
            progress[-1] = 0
    return (answers, progress)

def random_string(length):
    return ''.join(random.choice(HUMAN_FRIENDLY_CHARS) for x in range(length))

def clean(dirty_filename):
    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)

    # Replace accented characters with unaccented ones
    normalized_filename = unicodedata.normalize('NFKD', dirty_filename)

    # Strip out all characters that are not in @valid_chars
    cleaned_filename = ''.join([c for c in normalized_filename if c in valid_chars])

    return cleaned_filename
