# Python standard lib
import sys
from distutils.core import setup
from setuptools.command.test import test as TestCommand

# Package
import plan


class PyTest(TestCommand):
    # `$ python setup.py test' simply installs minimal requirements`
    # and runs the tests with no fancy stuff like parallel execution.
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--doctest-modules', '--verbose',
            './plan', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


# todo from pipfile
install_requires = None
tests_requires = None

setup(
    name='pyplan',
    packages=['pyplan'],
    version=plan.__version__,
    description=plan.__doc__.strip(),
    author=plan.__author__,
    author_email=plan.__email__,
    license=plan.__license__,
    url='https://github.com/CodePeasants/pyplan',
    download_url='',  # todo when first version is released.
    install_requires=install_requires,
    tests_requires=tests_requires,
    cmdclass={'test': PyTest},
    keywords=['plan', 'planner', 'event', 'schedule', 'party', 'tournament', 'time'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications'
    ],  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
)
