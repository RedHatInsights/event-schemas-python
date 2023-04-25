from setuptools import setup, find_packages

setup(
    name='crc-event-schemas',
    version='0.1.2',
    url='https://github.com/RedHatInsights/event-schemas-python',
    description='CloudEvents type bindings for console.redhat.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/x-rst',
    packages=find_packages(),
)
