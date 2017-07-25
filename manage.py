from flask_script import Manager, prompt_bool, Shell, Server

from botigo import app
from botigo import NAMESPACE

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def runserver():
    """ Run webserver. """
    app.run(debug=True)

if __name__ == '__main__':
    manager.run()
