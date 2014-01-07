Proto on Beanstalk
==================

This is a Git repository from which WebProto (a browser-accessible version of [Proto](http://proto.bbn.com/)) can be run in an autoscaling configuration on Amazon Elastic Beanstalk.

Details
-------

WebProto is mostly static content - the `static/` directory of this repository.
When it is time to compile a Proto program, the frontend JS calls back to the CGI script at `/webcompiler`.

This compiler is itself a compiled native binary.
Beanstalk does not support compiled applications directly.
As such, this implementation is a simple Flask application which serves all static content statically.
For the CGI script, it invokes `./p2b`, which was manually compiled on an AWS instance, and returns the result.

Running Proto-Beanstalk
-----------------------

This assumes:
* you have this repository cloned locally
* you have the elastic beanstalk tools (``eb``) installed
* you have an Amazon AWS account

First, get your repository set up; following [this documentation](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html)

* run ``eb init`` in the repository root.
  * enter your AWS access and secret keys
  * choose the US-East region
  * use the application name "proto-beanstalk"
  * use the environment name "proto-beanstalk-prod"
  * choose the "64bit Amazon Linux running Python" solution stack
  * choose "load balanced"
  * do not create an RDS DB
  * set up a default instance profile
* Run ``eb start``.  This will take a little while.
  Once it finishes, you should be able to find your new app in the beanstalk administrative console, if you care.
* Run ``eb status`` to see the URL for your site.

To make changes, edit things locally and run ``git aws.push`` to push a new version to the environment.

To clean up, run ``eb delete``.

Updating Static Data
--------------------

There is only one modification made to static/ from the original proto tarball.
In ``index.html``, the ``url`` parameter for the ``webcompiler`` is set to ``/webcompiler``, since Apache is configured by Beanstalk to treat ``/cgi-bin`` as a path to actual CGI scripts.

Building the Compiler
---------------------

Building the compiler is a little tricky, since it builds with a hard-coded path to its ``platform_ops`` and other files.
So it must be built with that path pointing to where those files will be placed by the Beanstalk infrastructure.

On an Amazon instance of the same type as used for Beanstalk (64-bit Amazon Linux), install the following:

```
yum install gcc gcc-c++ automake libtool libtool-ltdl-devel make
```

Then, from the root of the proto project:

* ``cd proto``
* ``libtoolize``
* ``./autogen.sh``
* ``./configure --prefix=/opt/python/current/app``
* ``make``

Unfortunately, proto does not support installs with DESTDIR, so we need to just install this in place and then extract from there.

* ``sudo make install``

Then copy `bin/p2b``, ``lib``, and ``share`` from ``/opt/python/current/app`` to the root of the proto-beanstalk project.

Bugs
----

Proto
.....

* Proto is not DESTDIR-compatible: registry generation assumes the install paths exist.
* Proto installs .a files, even though only .so files are used for plugins.

Beanstalk
.........

The [Amazon Docs](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html#command-options-python) would lead you to think that `` aws:elasticbeanstalk:container:python:staticfiles`` can be used to manage static files.
This is a lie.
It [doesn't work](http://stackoverflow.com/a/17436013/2737366).  

Instead, ``.ebextensions/custom-apache.config`` in this repository installs a custom Apache config to accomplish this, as suggested in the stackoverflow post.
