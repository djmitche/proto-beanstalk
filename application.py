import os
import flask
import subprocess

p2b_path = os.path.join(os.path.dirname(__file__), 'p2b')
p2b_path = './p2b'
 
application = flask.Flask(__name__)

#Set application.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
application.debug=True
 
@application.route('/')
def ui_redir():
    return flask.redirect(flask.url_for('static', filename='webproto/index.html'))

@application.route('/cgi-bin/webcompiler')
def webcompiler(program=None):
    program = flask.request.args.get('program')
    assert program is not None
    output = subprocess.Popen([p2b_path, '--instructions', program], stdout=subprocess.PIPE).communicate()[0]
    return flask.Response(output, mimetype="application/json")
 
if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
