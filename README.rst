=======
Impulse
=======

.. image:: https://img.shields.io/pypi/v/impulse.svg
    :target: https://pypi.org/project/impulse

.. image:: https://img.shields.io/pypi/pyversions/impulse.svg
    :alt: Python versions
    :target: https://pypi.org/project/impulse/

.. image:: https://api.travis-ci.com/seddonym/impulse.svg?branch=master
    :target: https://app.travis-ci.com/github/seddonym/impulse

* Free software: BSD license

Impulse is a command line tool for exploring the imports in a Python package.

It can be used to produce dependency graphs such as this:

.. image:: https://raw.githubusercontent.com/seddonym/impulse/master/docs/_static/images/flask.png
  :align: center
  :alt: Graph of flask package.

Installation
------------

Install Impulse
***************

::

    pip install impulse

Install the Python package you wish to analyse
**********************************************

::

    pip install somepackage

Command overview
----------------

There is currently only one command, feel free to suggest more by opening an issue or pull request.

``drawgraph``
*************

.. code-block:: text

    Usage: impulse drawgraph [OPTIONS] MODULE_NAME

    Options:
      --show-import-totals  Label arrows with the number of imports they represent.
      --help                Show this message and exit.

Draw a graph of the dependencies within any installed Python package or subpackage.

The graph shows the relationship between all the immediate children of the package. An arrow indicates that there is
at least one import by the child (or any of its descendants) from the subpackage where the arrow points.

The graph visualization is opened in a browser.

**Example**

.. code-block:: text

    impulse drawgraph django.db

.. image:: https://raw.githubusercontent.com/seddonym/impulse/master/docs/_static/images/django.db.png
  :align: center
  :alt: Graph of django.db package.

\

In this example, there is an arrow from ``django.db.models`` pointing to
``django.db.utils``.  This is because (along with one other import) ``django.db.models.constraints`` imports
``django.db.utils.DEFAULT_DB_ALIAS``.

\
\

**Example with import totals**

.. code-block:: text

    impulse drawgraph django.db --show-import-totals

.. image:: https://raw.githubusercontent.com/seddonym/impulse/master/docs/_static/images/django.db.show-import-totals.png
  :align: center
  :alt: Graph of django.db package with import totals.
