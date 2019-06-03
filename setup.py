from setuptools import setup, find_packages

setup(
    name='sncf-cli',
    version='0.1',
    description='Search SNCF journeys from the CLI',
    url='https://github.com/yafeunteun/sncf-cli',
    author='Yann Feunteun, Maxime Mouchet',
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'dateparser',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        sncf-cli=locomotive.cli:cli
    '''
)
