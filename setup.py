import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version:
    VERSION = version.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='prayer_times',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='',
    long_description=README,
    url='https://www.example.com/',
    author='guneysus',
    author_email='g.seref@yahoo.ca',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: bottle',
        'Framework :: bottle :: 0.12.16',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ], install_requires="""
bottle==0.12.16
suds-py3==1.3.3.0
""",
)
