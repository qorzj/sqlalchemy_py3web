#!/usr/bin/env python

from setuptools import setup

setup(name='sqlalchemy_py3web',
       version='0.1.5',
       description='sqlalchemy_py3web is a sqlalchemy plugin for py3web',
       author='qorzj',
       author_email='inull@qq.com',
       maintainer='qorzj',
       maintainer_email='inull@qq.com',
       url='https://github.com/qorzj/sqlalchemy_py3web',
       keywords='py3web sqlalchemy plugin sqlalchemy_plugin',
       packages=['sqlalchemy_plugin'],
       long_description="sqlalchemy_py3web is a sqlalchemy plugin for py3web",
       license="Public domain",
       platforms=["any"],
       install_requires=["SQLAlchemy"],
      )

