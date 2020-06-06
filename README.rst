findd |travis|_ |coveralls|_
============================

Find duplicate files, based on size and hashvalues.

Install
^^^^^^^

.. code-block:: bash

   pip install findd


Usage
^^^^^

.. code-block::

   findd --help

   usage: findd [-h] [--version] {init,update,list,run} ...

   positional arguments:
     {init,update,list,run}
       init                create a new Findd project
       update              update the index
       list                list duplicates tracked by the index
       run                 run a command for duplicates tracked by the index

   optional arguments:
     -h, --help            show this help message and exit
     --version             show program's version number and exit

   Report findd bugs to <https://github.com/schnittstabil/findd/issues>
   findd home page: <https://github.com/schnittstabil/findd>


Typical Workflow
^^^^^^^^^^^^^^^^

.. code-block:: bash

   mkdir temp
   cd temp
   findd init
   ls -A
   # .findd


   # create some duplicates
   mkdir directory
   echo a > directory/a.txt
   echo b > directory/b.txt
   echo c > directory/c.txt
   cp -r directory directory_copy
   tree -a
   # .
   # ├── directory
   # │   ├── a.txt
   # │   ├── b.txt
   # │   └── c.txt
   # └── directory_copy
   #     ├── a.txt
   #     ├── b.txt
   #     └── c.txt


   findd update -v
   # scanning db 100% |#####################################################|
   # scanning fs      |#####################################################|
   # hashing     100% |#####################################################|


   findd list
   # 'directory/a.txt' 'directory_copy/a.txt'
   # 'directory/c.txt' 'directory_copy/c.txt'
   # 'directory/b.txt' 'directory_copy/b.txt'


   # remove a duplicate
   rm 'directory_copy/c.txt'


   findd update
   findd list
   # 'directory/a.txt' 'directory_copy/a.txt'
   # 'directory/b.txt' 'directory_copy/b.txt'


License
^^^^^^^

Copyright © 2015 Michael Mayer

Licensed under the `MIT License <https://github.com/schnittstabil/findd/blob/master/LICENSE>`_.

.. |coveralls| image:: https://coveralls.io/repos/schnittstabil/findd/badge.svg?branch=master&service=github
.. _coveralls: https://coveralls.io/github/schnittstabil/findd
.. |travis| image:: https://travis-ci.org/schnittstabil/findd.svg?branch=master
.. _travis: https://travis-ci.org/schnittstabil/findd
