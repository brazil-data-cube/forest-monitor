import contextlib
import os
from flask_script import Manager
from pathlib import Path
from bdc_core.decorators.utils import working_directory
from forest_monitor import app


manager = Manager(app)


@manager.command
def run():
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('PORT', '5000'))
    except ValueError:
        PORT = 5000

    app.run(HOST, PORT)


@manager.command
def docs(serve=False, port=5001):
    import subprocess
    from http.server import test, CGIHTTPRequestHandler
    from pathlib import Path

    docs_directory = Path(os.path.abspath(os.path.dirname(__file__))) / 'docs'

    with working_directory(str(docs_directory)):
        # Generate Documentation through Makefile
        subprocess.call('make html', shell=True)

    if serve:
        with working_directory(str(docs_directory / 'build/html')):
            test(HandlerClass=CGIHTTPRequestHandler, port=int(port), bind='')


if __name__ == '__main__':
    manager.run()
