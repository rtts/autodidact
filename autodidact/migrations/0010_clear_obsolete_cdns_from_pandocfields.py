from django.db import migrations
import sys

def resave_all_pandoc_fields(apps, schema_editor):

    # This migration doesn't reference any historical fields, so
    # directly importing these should be safe
    from autodidact.models import Page, Course, Topic, Session, Step, Clarification

    print('To scrub the database from obsolete MathJax CDN URLs, all objects will now be re-saved to trigger regeneration of Pandoc HTML.')

    for klass in [Page, Course, Topic, Session, Step, Clarification]:
        print("    Re-saving {}s: ".format(klass.__name__), end='')
        obj = None
        for obj in klass.objects.all():
            sys.stdout.write('.')
            sys.stdout.flush()
            obj.save()
        if obj is None:
            print('(none exist)')
        else:
            print(' done')
    print()

class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0009_stepfile'),
    ]

    operations = [
        migrations.RunPython(resave_all_pandoc_fields, migrations.RunPython.noop),
    ]
