Autodidact
==========

Autodidact is simple content-management system (CMS) for creating
self-learning activities. It is used at Tilburg University for the
"Best Practices in Statistics" series of lab sessions, soon to be made
available to the general public at https://bps.uvt.nl/

Installation
------------

Autodidact is written in Python using the Django framework. A separate
repository -- autodidact-config -- contains a script that packages
Autodidact's source code into a Debian .deb package for easy
installation. Alternatively, you can deploy Autodidact like any
ordinary Django project -- see the installation instructions at
https://docs.djangoproject.com/en/1.7/howto/deployment/

Usage
-----

Simply point your webbrowser to the host you have installed Autodidact
on and login with the credentials you received during the installation
process. You will be presented with the default Django Admin site
where you can start adding students and content.

Documentation
-------------

The Admin site includes an on-line help system with documentation
about the various components of Autodidact. Many things should be
self-explanatory, though.

Hacking
-------

It is highly encouraged to transform Autodidact into your own custom
learning solution. For starters you should adapt the default templates
to your liking. You could also use the "autodidact" app inside your
own Django project, or use this project as a starting point to
develop your own learning platform. Happy hacking!