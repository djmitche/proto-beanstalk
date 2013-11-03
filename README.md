Proto on Beanstalk
==================

This is a Git repository from which WebProto (a browser-accessible version of [Proto](http://proto.bbn.com/)) can be run in an autoscaling configuration on Amazon Elastic Beanstalk.

Details
-------

WebProto is mostly static content - the `static/` directory of this repository.
When it is time to compile a Proto program, the frontend JS calls back to the CGI script at `/cgi-bin/webcompiler`.

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
* Run ``eb statis`` to see the URL for your site.

To make changes, edit things locally and run ``git aws.push`` to push a new version to the environment.

To clean up, run ``eb delete``.
