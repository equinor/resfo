Building from source and running the tests
==========================================

resfo is set up to use tox which can simplify development,
but all that is necessary in order to get started is git, pip and python:

First, install resfo in editable mode:

.. code-block:: console

    git clone git@github.com:equinor/resfo.git
    cd resfo
    pip install -e .

Second, install the dev-requirements.txt, which contains the packages resfo
require in order to run tests:

.. code-block:: console

    pip install -e ".[dev]"

At last, you can use pytest to run the tests

.. code-block:: console

    pytest tests
