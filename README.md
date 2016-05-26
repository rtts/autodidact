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

1. Add `"autodidact"` to your installed apps:

        INSTALLED_APPS += ["autodidact"]

2. Add `autodidact.urls` to your URL patterns:

        urlpatterns += [url(r'^', include(autodidact.urls)]

3. Provide a base template. As a starting point, feel free to use [the
template in use at Tilburg University](https://github.com/JaapJoris/autodidact/blob/master/bps/templates/base.html).

4. Start your development server (`./manage.py runserver`) and visit
http://localhost:8000/admin/autodidact/page/add/ to add a
homepage. Hit "Save" and you will redirected to the newly created
homepage.

5. Visit http://localhost:8000/admin and have a look at the database
tables. The most important ones are, listed in hierarchical order:
Programmes, Courses, Sessions, Assignments, and Steps. Autodidact was
designed to hide the admin from the user as much as possible, that's
why you will be redirected to the website after saving most
objects. Once you've added a Programme and a Course, you won't need to
visit the admin again and can just use the appropriate "add" and
"edit" links that are present throughout the website.

6. Have fun! If you have any questions or bug reports, feel free to
contact the author or submit a Github issue.
