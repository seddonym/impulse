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

.. image:: https://img.shields.io/badge/License-BSD_2--Clause-orange.svg
    :target: https://opensource.org/licenses/BSD-2-Clause

Impulse is a command line tool for exploring the imports in a Python package.

Running it will open up the graph in a browser window, along with download links for SVG and PNG.

Screenshot
------------

.. image:: https://raw.githubusercontent.com/seddonym/impulse/master/docs/_static/images/screenshot.png
  :align: center
  :alt: Graph of django.db.

\

Installation
------------

1. Install Impulse using your favorite Python package manager. E.g., with ``pip``::

    pip install impulse

2. Ensure the package under test is importable, e.g. by changing your working directory to the one containing the
package, or installing it via a Python package manager.

One liner using ``uv tool``
***************************

If you use `uv <https://docs.astral.sh/uv/>`_ you can run it with this one-liner, without needing to install anything.
::

    uv tool run --with=PACKAGE impulse drawgraph MODULE_NAME

Command overview
----------------

There is currently only one command.

``drawgraph``
*************

.. code-block:: text

    Usage: impulse drawgraph [OPTIONS] MODULE_NAME

    Options:
      --show-import-totals   Label arrows with the number of imports they
                             represent.
      --show-cycle-breakers  Identify a set of dependencies that, if removed,
                             would make the graph acyclic, and display them as
                             dashed lines.
      --help                 Show this message and exit.

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

In this example, there is an arrow from ``.models`` to
``.utils``.  This is because (along with one other import) ``django.db.models.constraints`` imports
``django.db.utils.DEFAULT_DB_ALIAS``.

\
\

**Example with import totals**

.. code-block:: text

    impulse drawgraph django.db --show-import-totals

.. image:: https://raw.githubusercontent.com/seddonym/impulse/master/docs/_static/images/django.db.show-import-totals.png
  :align: center
  :alt: Graph of django.db package with import totals.

Here you can see that there are two imports from modules within ``django.db.models`` of modules
within ``django.db.utils``.
\
\

**Example with cycle breakers**

.. code-block:: text

    impulse drawgraph django.db --show-cycle-breakers

.. image:: https://raw.githubusercontent.com/seddonym/impulse/master/docs/_static/images/django.db.show-cycle-breakers.png
  :align: center
  :alt: Graph of django.db package with cycle breakers.

Here you can see that two of the dependencies are shown as a dashed line. If these dependencies were to be
removed, the graph would be acyclic. To decide on the cycle breakers, Impulse uses the
`nominate_cycle_breakers method provided by Grimp <https://grimp.readthedocs.io/en/stable/usage.html#ImportGraph.nominate_cycle_breakers>`_.