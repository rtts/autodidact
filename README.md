Autodidact
==========

Autodidact is simple content-management system (CMS) for creating
self-learning activities. It is used at Tilburg University for the
"Best Practices in Statistics" (BPS) series of lab sessions, available
to Tilburg University students at https://bps.uvt.nl/

Autodidact is written in Python using the Django framework. It is a
reusable Django *app* for use in your own projects. There is also a
separate repository called [BPS](https://github.com/JaapJoris/bps)
which contains the Django *project* currently deployed at Tilburg
University. You may find it of use as a reference project or as a
starting point for your own projects.

Several other projects have spun off from Autodidact. First, there is
[django-pandocfield](https://github.com/JaapJoris/django-pandocfield)
that is used by Autodidact compile Markdown and LaTeX markup. Second,
there is [django-numberedmodel](https://github.com/JaapJoris/django-numberedmodel),
a simple app to automatically number model instances. These apps will automatically
be installed using the installation procedure below.

Installation
------------

Tilburg University maintains a Debian repository at
https://non-gnu.uvt.nl/ from which Autodidact can be installed. First,
add the following lines to `/etc/apt/sources.list`:

    deb http://non-gnu.uvt.nl/debian jessie uvt
    deb-src http://non-gnu.uvt.nl/debian jessie uvt

Second, add the Tilburg University signing key to your apt key store:

    curl https://non-gnu.uvt.nl/debian/uvt_key.asc | apt-key add -

Now you can install the `autodidact` package with `apt-get`:

    apt-get install autodidact

Congratulations, the Autodidact Django app has now been installed and
is ready to use in your own projects!

Configuration
-------------

1. Add the following apps to your `INSTALLED_APPS`:

        INSTALLED_APPS += [
            "autodidact",
            "pandocfield",
            "numberedmodel",
        ]

2. Add the following urls to your URL patterns:

        urlpatterns = patterns('',
            url(r'^admin/', include(admin.site.urls)),
            url(r'^accounts/login/$', django.contrib.auth.views.login),
            url(r'^accounts/logout/$', django.contrib.auth.views.logout),
            url(r'^', include(autodidact.urls)),
        )

3. Make sure that `django.core.context_processors.request` is included in your `TEMPLATE_CONTEXT_PROCESSORS`:

        TEMPLATE_CONTEXT_PROCESSORS = [
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.tz',
            'django.core.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]

    (Or, in newer Django versions using the [TEMPLATES](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES) setting)

4. Run the database migrations and create the first Django user if you haven't already:

        $ ./manage.py migrate
        $ ./manage.py createsuperuser

5. You're all set! Start the development server (`./manage.py runserver`) and visit
[http://localhost:8000/](http://localhost:8000/). In the admin you can add Programs, Courses, Sessions, Assignments, and Steps. Have fun! If you have any questions or bug reports, feel free to
contact the author or submit a Github issue.
