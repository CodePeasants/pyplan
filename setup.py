from distutils.core import setup


setup(
    name='pyplan',
    packages=['pyplan'],
    version='0.1.0',
    description='API for planning events.',
    author='CodePeasants',
    author_email='codepeasants@gmail.com',
    url='https://github.com/CodePeasants/pyplan',
    download_url='',  # todo when first version is released.
    keywords=['plan', 'planner', 'event', 'schedule', 'party', 'tournament', 'time'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications'
    ],  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
)
