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

After installation, please specify the database credentials and other
configuration options in `/etc/bps/config.ini`. You can call the
regular Django database management commands from inside the project
directory `/usr/share/bps`. A configuration file has been included for
the Apache web server. Enable it with the following commands:

    sudo apt-get install apache2 libapache2-mod-wsgi
    cd /etc/apache2/conf-enabled
    sudo ln -s ../conf-available/bps.conf
    sudo systemctl restart apache2

BPS should now be up and running!

Hacking
-------

It is highly encouraged to transform Autodidact into your own custom
learning solution. For starters you should adapt the default templates
to your liking. You can easily include the "autodidact" app in an
existing Django project, or use the BPS project as a starting point to
develop your own learning platform. Happy hacking!
