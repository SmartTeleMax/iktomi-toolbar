# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='iktomi.cms',
    version='0.1',
    packages=['iktomi', 'iktomi.cms'],
    requires=[
        'webob (>1.1b1)',
        'iktomi (>0.3)',
    ],
    author='Roman Gladkov',
    author_email='d1ffuz0r@gmail.com',
    maintainer='Harutyun Dagesyan',
    maintainer_email='me@harutune.name',
    description='Debug toolbar for iktomi.',
    #long_description=open('README').read(),
    url='http://github.com/SmartTeleMax/iktomi_toolbar/',
    license='MIT',
    #keywords='',
)
