
What is Tox?
--------------------


.. image:: https://img.shields.io/pypi/v/tox.svg
   :target: https://pypi.org/project/tox/
.. image:: https://img.shields.io/pypi/pyversions/tox.svg
  :target: https://pypi.org/project/tox/
.. image:: https://travis-ci.org/tox-dev/tox.svg?branch=master
    :target: https://travis-ci.org/tox-dev/tox
.. image:: https://img.shields.io/appveyor/ci/RonnyPfannschmidt/tox/master.svg
    :target: https://ci.appveyor.com/project/RonnyPfannschmidt/tox


Tox is a generic virtualenv management and test command line tool you can use for:

* checking your package installs correctly with different Python versions and
  interpreters

* running your tests in each of the environments, configuring your test tool of choice

* acting as a frontend to Continuous Integration servers, greatly
  reducing boilerplate and merging CI and shell-based testing.

For more information and the repository please checkout:

- home and docs: https://tox.readthedocs.org

- repository: https://github.com/tox-dev/tox



Changelog (last 5 releases - `full changelog <https://github.com/tox-dev/tox/blob/master/CHANGELOG>`_)
======================================================================================================


2.7.0
-----

- `#p450 <https://github.com/tox-dev/tox/pull/450>`_: Stop after the first installdeps and first testenv create hooks
  succeed. This changes the default behaviour of `tox_testenv_create`
  and `tox_testenv_install_deps` to not execute other registered hooks when
  the first hook returns a result that is not `None`.
  Thanks Anthony Sottile (@asottile).

- `#271 <https://github.com/tox-dev/tox/issues/271>`_ and `#464 <https://github.com/tox-dev/tox/issues/464>`_: Improve environment information for users.

  New command line parameter: `-a` show **all** defined environments -
  not just the ones defined in (or generated from) envlist.

  New verbosity settings for `-l` and `-a`: show user defined descriptions
  of the environments. This also works for generated environments from factors
  by concatenating factor descriptions into a complete description.

  Note that for backwards compatibility with scripts using the output of `-l`
  it's output remains unchanged.

  Thanks Gábor Bernát (@gaborbernat).

- `#464 <https://github.com/tox-dev/tox/issues/464>`_: Fix incorrect egg-info location for modified package_dir in setup.py.
  Thanks Selim Belhaouane (@selimb).

- `#431 <https://github.com/tox-dev/tox/issues/431>`_: Add 'LANGUAGE' to default passed environment variables.
  Thanks Paweł Adamczak (@pawalad).

- `#455 <https://github.com/tox-dev/tox/issues/455>`_: Add a Vagrantfile with a customized Arch Linux box for local testing.
  Thanks Oliver Bestwalter (@obestwalter).

- `#454 <https://github.com/tox-dev/tox/issues/454>`_: Revert `#407 <https://github.com/tox-dev/tox/issues/407>`_, empty commands is not treated as an error.
  Thanks Anthony Sottile (@asottile).

- `#446 <https://github.com/tox-dev/tox/issues/446>`_: (infrastructure) Travis CI tests for tox now also run on OS X now.
  Thanks Jason R. Coombs (@jaraco).

2.6.0
-----

- add "alwayscopy" config option to instruct virtualenv to always copy
  files instead of symlinking. Thanks Igor Duarte Cardoso (@igordcard).

- pass setenv variables to setup.py during a usedevelop install.
  Thanks Eli Collins (@eli-collins).

- replace all references to testrun.org with readthedocs ones.
  Thanks Oliver Bestwalter (@obestwalter).

- fix `#323 <https://github.com/tox-dev/tox/issues/323>`_ by avoiding virtualenv14 is not used on py32
  (although we don't officially support py32).
  Thanks Jason R. Coombs (@jaraco).

- add Python 3.6 to envlist and CI.
  Thanks Andrii Soldatenko (@andriisoldatenko).

- fix glob resolution from TOX_TESTENV_PASSENV env variable
  Thanks Allan Feldman (@a-feld).

2.5.0
-----

- slightly backward incompatible: fix `#310 <https://github.com/tox-dev/tox/issues/310>`_: the {posargs} substitution
  now properly preserves the tox command line positional arguments. Positional
  arguments with spaces are now properly handled.
  NOTE: if your tox invocation previously used extra quoting for positional arguments to
  work around `#310 <https://github.com/tox-dev/tox/issues/310>`_, you need to remove the quoting. Example:
  tox -- "'some string'"  # has to now be written simply as
  tox -- "some string"
  thanks holger krekel.  You can set ``minversion = 2.5.0`` in the ``[tox]``
  section of ``tox.ini`` to make sure people using your tox.ini use the correct version.

- fix `#359 <https://github.com/tox-dev/tox/issues/359>`_: add COMSPEC to default passenv on windows.  Thanks
  @anthrotype.

- add support for py36 and py37 and add py36-dev and py37(nightly) to
  travis builds of tox. Thanks John Vandenberg.

- fix `#348 <https://github.com/tox-dev/tox/issues/348>`_: add py2 and py3 as default environments pointing to
  "python2" and "python3" basepython executables.  Also fix `#347 <https://github.com/tox-dev/tox/issues/347>`_ by
  updating the list of default envs in the tox basic example.
  Thanks Tobias McNulty.

- make "-h" and "--help-ini" options work even if there is no tox.ini,
  thanks holger krekel.

- add {:} substitution, which is replaced with os-specific path
  separator, thanks Lukasz Rogalski.

- fix `#305 <https://github.com/tox-dev/tox/issues/305>`_: ``downloadcache`` test env config is now ignored as pip-8
  does caching by default. Thanks holger krekel.

- output from install command in verbose (-vv) mode is now printed to console instead of
  being redirected to file, thanks Lukasz Rogalski

- fix `#399 <https://github.com/tox-dev/tox/issues/399>`_.  Make sure {envtmpdir} is created if it doesn't exist at the
  start of a testenvironment run. Thanks Manuel Jacob.

- fix `#316 <https://github.com/tox-dev/tox/issues/316>`_: Lack of commands key in ini file is now treated as an error.
  Reported virtualenv status is 'nothing to do' instead of 'commands
  succeeded', with relevant error message displayed. Thanks Lukasz Rogalski.

2.4.1
-----

- fix `#380 <https://github.com/tox-dev/tox/issues/380>`_: properly perform substitution again. Thanks Ian
  Cordasco.

2.4.0
-----

- remove PYTHONPATH from environment during the install phase because a
  tox-run should not have hidden dependencies and the test commands will also
  not see a PYTHONPATH.  If this causes unforeseen problems it may be
  reverted in a bugfix release.  Thanks Jason R. Coombs.

- fix `#352 <https://github.com/tox-dev/tox/issues/352>`_: prevent a configuration where envdir==toxinidir and
  refine docs to warn people about changing "envdir". Thanks Oliver Bestwalter and holger krekel.

- fix `#375 <https://github.com/tox-dev/tox/issues/375>`_, fix `#330 <https://github.com/tox-dev/tox/issues/330>`_: warn against tox-setup.py integration as
  "setup.py test" should really just test with the current interpreter. Thanks Ronny Pfannschmidt.

- fix `#302 <https://github.com/tox-dev/tox/issues/302>`_: allow cross-testenv substitution where we substitute
  with ``{x,y}`` generative syntax.  Thanks Andrew Pashkin.

- fix `#212 <https://github.com/tox-dev/tox/issues/212>`_: allow escaping curly brace chars "\{" and "\}" if you need the
  chars "{" and "}" to appear in your commands or other ini values.
  Thanks John Vandenberg.

- addresses `#66 <https://github.com/tox-dev/tox/issues/66>`_: add --workdir option to override where tox stores its ".tox" directory
  and all of the virtualenv environment.  Thanks Danring.

- introduce per-venv list_dependencies_command which defaults
  to "pip freeze" to obtain the list of installed packages.
  Thanks Ted Shaw, Holger Krekel.

- close `#66 <https://github.com/tox-dev/tox/issues/66>`_: add documentation to jenkins page on how to avoid
  "too long shebang" lines when calling pip from tox.  Note that we
  can not use "python -m pip install X" by default because the latter
  adds the CWD and pip will think X is installed if it is there.
  "pip install X" does not do that.

- new list_dependencies_command to influence how tox determines
  which dependencies are installed in a testenv.

- (experimental) New feature: When a search for a config file fails, tox tries loading
  setup.cfg with a section prefix of "tox".

- fix `#275 <https://github.com/tox-dev/tox/issues/275>`_: Introduce hooks ``tox_runtest_pre``` and
  ``tox_runtest_post`` which run before and after the tests of a venv,
  respectively. Thanks to Matthew Schinckel and itxaka serrano.

- fix `#317 <https://github.com/tox-dev/tox/issues/317>`_: evaluate minversion before tox config is parsed completely.
  Thanks Sachi King for the PR.

- added the "extras" environment option to specify the extras to use when doing the
  sdist or develop install. Contributed by Alex Grönholm.

- use pytest-catchlog instead of pytest-capturelog (latter is not
  maintained, uses deprecated pytest API)


