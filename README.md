Autodidact
==========

Autodidact is simple content-management system (CMS) for creating
self-learning activities. It is used at Tilburg University for the
"Best Practices in Statistics" (BPS) series of lab sessions, soon to
be made available to the general public at https://bps.uvt.nl/

Autodidact is written in Python using the Django framework. It is a
reusable Django *app* for use in your own projects. This repository
also includes the Django *project* "BPS", which contains all code
specific to the BPS web application.

Installation
------------

Tilburg University maintains a Debian repository at
https://non-gnu.uvt.nl/ from which both Autodidact and BPS can be
installed.

1. First, add the following lines to `/etc/apt/sources.list`:

    deb http://non-gnu.uvt.nl/debian jessie uvt
    deb-src http://non-gnu.uvt.nl/debian jessie uvt

2. Second, add the Tilburg University signing key to your apt key store:

    curl http://non-gnu.uvt.nl/debian/uvt_key.asc | apt-key add -

3. Now you can install the `autodidact` package with `apt-get`:

    apt-get install autodidact

Congratulations, the Autodidact Django app has now been installed and
is ready to use in your own projects!

Deploying the BPS project
-------------------------

To run the included BPS project, a few additional steps are
needed. First, please open the configuration file
`/etc/bps/config.ini` and check if the default values are suitable for
your situation (for testing purposes they are, but for a production
server you probably want to use a "real" database and adjust the
`allowed_hosts` setting). Now the database tables can be created with
the following commands:

    cd /usr/lib/python2.7/dist-packages/bps/
    python manage.py migrate

Second, you will have to create at least one superuser:

    python manage.py createsuperuser

Finally, Apache needs to be configured to serve BPS. For this purpose,
a basic configuration file has already been installed in
`/etc/apache2/conf-enabled/bps.conf`. All you have to do is restart
Apache:

    systemctl restart apache2

BPS should now be up and running! Visit the URL /admin/ and log in
with your superuser credentials to start adding users and course
content.
