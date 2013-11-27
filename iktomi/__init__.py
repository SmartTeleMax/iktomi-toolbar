# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='iktomi.toolbar',
    version='0.1',
    packages=['iktomi', 'iktomi.toolbar'],
    requires=[
        'iktomi (>0.3)',
    ],
    author='Roman Gladkov',
    author_email='d1ffuz0r@jabber.ru',
    maintainer='Harut Dagesyan',
    maintainer_email='me@harutune.name',
    description='Debug toolbar for iktomi.',
    #long_description=open('README').read(),
    url='http://github.com/SmartTeleMax/iktomi_toolbar/',
    license='MIT',
    #keywords='',
)
