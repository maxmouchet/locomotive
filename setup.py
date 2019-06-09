import os

from setuptools import find_packages, setup

fp = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')
with open(fp, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sncf-cli',
    description='Search SNCF journeys from the CLI.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yafeunteun/sncf-cli',
    author='Yann Feunteun, Maxime Mouchet',
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.csv', '*.mustache'],
    },
    install_requires=[
        'attrs',
        'chevron',
        'Click',
        'dateparser',
        'geopy',
        'pandas',
        'requests',
    ],
    extras_require={
        'dev': [
            'black',
            'mypy',
            'pylint',
            'pytest-cov'
        ]
    },
    python_requires='>=3',
    entry_points='''
        [console_scripts]
        sncf-cli=locomotive.cli:cli
    '''
)
