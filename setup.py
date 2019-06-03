from setuptools import setup, find_packages

setup(
    name='sncf-cli',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'dateparser',
        'numpy',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        sncf-cli=locomotive.cli:cli
    '''
)
