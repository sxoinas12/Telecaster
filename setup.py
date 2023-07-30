import sys
from distutils.cmd import Command
from subprocess import check_call
from typing import List

from setuptools import setup, find_packages


class CustomCommand(Command):
    user_options: List[str] = []
    description = 'Custom command'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class DevelopCommand(CustomCommand):
    def run(self):
        print('Do not try to install telecaster. Run `pip install -r requirements.txt` instead.')  # noqa
        sys.exit(1)


class LocalCommand(CustomCommand):
    def run(self):
        print('Do not try to install telecaster. Run `pip install -r requirements-dev.txt` instead.')  # noqa
        sys.exit(1)


def create_command(text: str, commands: List[List[str]]):
    class GeneratedCommand(CustomCommand):
        description = text

        def run(self):
            for cmd in commands:
                check_call(cmd)

    return GeneratedCommand


setup(
    name='telecaster',
    version='1.0',
    packages=find_packages(),
    scripts=['manage.py'],
    cmdclass=dict(
        develop=DevelopCommand,
        local=LocalCommand,
        fix=create_command(
            'Auto-fixes and lints code',
            [
                ['python', 'setup.py', 'format'],
                ['python', 'setup.py', 'lint'],
                ['python', 'setup.py', 'lint_types'],
                ['python', 'setup.py', 'format_docstrings'],
            ],
        ),
        verify=create_command(
            'Verifies that code is valid',
            [
                ['python', 'setup.py', 'verify_format'],
                ['python', 'setup.py', 'lint'],
                ['python', 'setup.py', 'lint_types'],
                ['python', 'setup.py', 'verify_format_docstrings'],
            ],
        ),
        format=create_command('Auto-formats code', [['black', '-S', '--config', './pyproject.toml', '.']]),
        verify_format=create_command(
            'Verifies that code is properly formatted',
            [['black', '-S', '--check', '--config', './pyproject.toml', '.']],
        ),
        format_docstrings=create_command(
            'Auto-formats doc strings', [['docformatter', '-r', '-e', 'env', 'venv', '-i', '.']]
        ),
        verify_format_docstrings=create_command(
            'Verifies that doc strings are properly formatted',
            [['docformatter', '-r', '-e', 'env', 'venv', 'node_modules', '-c', '.']],
        ),
        lint=create_command('Lints the code', [['flake8', '.']]),
        lint_types=create_command(
            'Type checks the code',
            [
                ['mypy', 'telecaster', '--strict', '--config-file', './setup.cfg'],
            ],
        ),
    ),
)
