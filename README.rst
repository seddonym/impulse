=======
Impulse
=======

.. image:: https://img.shields.io/pypi/v/impulse.svg
    :target: https://pypi.org/project/impulse

.. image:: https://img.shields.io/pypi/pyversions/impulse.svg
    :alt: Python versions
    :target: https://pypi.org/project/impulse/

.. image:: https://api.travis-ci.org/seddonym/impulse.svg?branch=master
    :target: https://travis-ci.org/seddonym/impulse

* Free software: BSD license

Impulse is a command line tool for exploring the imports in a Python package.

It can be used to produce dependency graphs such as this:

.. image:: https://raw.githubusercontent.com/seddonym/impulse/drawgraph-docs/docs/_static/images/flask.png
  :align: center
  :alt: Graph of flask package.

**Warning:** This software is currently in beta. It is undergoing active development, and breaking changes may be
introduced between versions.

Installation
------------

Install Impulse::

    pip install impulse

Install the Python package you wish to analyse::

    pip install somepackage


Command overview
----------------

There is currently only one command, feel free to suggest more by opening an issue or pull request.

``drawgraph``
*************

Draw a graph of the dependencies within any installed Python package or subpackage.

**Command**::

    impulse drawgraph django.db

**Output:**

.. image:: https://raw.githubusercontent.com/seddonym/impulse/drawgraph-docs/docs/_static/images/django.db.png
  :align: center
  :alt: Graph of django.db package.