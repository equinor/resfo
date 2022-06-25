Building from source and running the tests
==========================================

ecl-data-io is set up to use tox which can simplify development,
but all that is necessary in order to get started is git, pip and python:

First, install ecl-data-io in editable mode:

.. code-block:: console

git clone git@github.com:equinor/ecl-data-io.git
cd ecl-data-io
pip install -e .

Second, install the dev-requirements.txt, which contains the packages ecl-data-io
require in order to run tests:

.. code-block:: console

pip install -r dev-requirements.txt

At last, you can use pytest to run the tests

.. code-block:: console

pytest tests
