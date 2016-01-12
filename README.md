Autodidact
==========

Autodidact is simple content-management system (CMS) for creating
self-learning activities. It is used at Tilburg University for the
"Best Practices in Statistics" (BPS) series of lab sessions, soon to
be made available to the general public at https://bps.uvt.nl/

Installation
------------

Autodidact is written in Python using the Django framework. It is a
reusable Django *app* for use in your own projects. This repository
also includes the Django *project* "BPS", which contains all code
specific to the BPS web application. You can create a Debian package
that contains both Autodidact and BPS with the following commands:

    sudo apt-get install devscripts
    debuild -us -uc

You can then install the package with:

    sudo debi

Congratulations, the Autodidact django application has now been
installed and is ready to use in your own projects!

Deploying the BPS project
-------------------------

To run the included BPS project, a few additional steps are
needed. First, please create a database using your favorite database
management system. You can specify the database credentials in the
file `/etc/bps/config.ini`. Now the database tables can be created
with the following commands:

    cd /usr/lib/python2.7/dist-packages/bps/
    ./manage.py migrate

Second, you will have to create at least one superuser:

    ./manage.py createsuperuser

Finally, Apache needs to be configured to serve BPS. For this purpose,
a configuration file has already been included. Enable it with the
following commands:

    sudo apt-get install apache2 libapache2-mod-wsgi
    cd /etc/apache2/conf-enabled
    sudo ln -s ../conf-available/bps.conf
    sudo systemctl restart apache2

BPS should now be up and running!
