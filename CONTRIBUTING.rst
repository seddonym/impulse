============
Contributing
============

We welcome contributions to Impulse.

Bug reports
===========

When `reporting a bug <https://github.com/seddonym/impulse/issues>`_ please include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * Detailed steps to reproduce the bug.

Feature requests and feedback
=============================

The best way to send feedback is to file an issue at https://github.com/seddonym/impulse/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible.
* Remember that this is a volunteer-driven project.

Submitting pull requests
========================

Before spending time working on a pull request, we highly recommend filing a Github issue and engaging with the
project maintainer (David Seddon) to align on the direction you're planning to take. This can save a lot of your
precious time!

This doesn't apply to trivial pull requests such as spelling corrections.

Before requesting review you should:

1. Update documentation when there's new API, functionality etc.
2. Add a note to ``CHANGELOG.rst`` about the changes.
3. Add yourself to ``AUTHORS.rst`` under a _Contributors_ section.
4. Run ``just check``.

Development
===========

System prerequisites
--------------------

Make sure these are installed first.

- `git <https://github.com/git-guides/install-git>`_
- `uv <https://docs.astral.sh/uv/#installation>`_
- `just <https://just.systems/man/en/packages.html>`_

Setup
-----

You don't need to activate or manage a virtual environment - this is taken care in the background of by ``uv``.

1. Fork `impulse <https://github.com/seddonym/impulse>`_
   (look for the "Fork" button).
2. Clone your fork locally::

    git clone git@github.com:your_name_here/impulse.git

3. Change into the directory you just cloned::

    cd impulse

4. Set up pre-commit. (Optional, but recommended.)::

    just install-precommit


You will now be able to run commands prefixed with ``just``, providing you're in the ``impulse`` directory.
To see available commands, run ``just``.

Formatting code
---------------

::

    just format

Running linters
---------------

::

    just lint

Running tests
-------------

Currently the project is very small and relies on a single smoke test, which runs the tool on the ``grimp`` package.
If you're developing a new feature we will probably need to expand that: just reach out and we'll make sure we have
a testing framework in place.

In the meantime, you can run the test like this::

    just test


Before you push
---------------

It's a good idea to run ``just check`` before getting a review. This will run linters, docs build and tests under
every supported Python version.

Building documentation
----------------------

To build docs and open them in a browser::

    just build-and-open-docs

Or, if you just want to build them::

    just build-docs

