|Build Status| |Code Coverage| |Code Climate|

S3 Cache for Python
===================

`Niall McCarroll <http://www.mccarroll.net/>`__ wrote a neat little `AWS
S3 cache <http://www.mccarroll.net/snippets/s3boto/index.html>`__ on his
blog that I found really useful, but could not find on
`PyPI <https://pypi.python.org/pypi>`__, so here it is in a refactored
form as a public service.

Instructions
------------

::

    from s3cache import S3Cache

    s3 = S3Cache("/tmp", "t13d-misc")
    s3.connect()
    s3.create_bucket()
    assert(s3.bucket_exists())

    s3.set_verbosity(True)
    s3.set_caching(True)

    f = s3.open("/tmp/world.txt", "w")
    f.write("Hello")
    f.close()

    f = s3.open("/tmp/world.txt", "a")
    f.write(" World")
    f.close()

    f2 = s3.open("/tmp/world.txt", "r")
    f2.close()

    assert(s3.object_exists("/tmp/world.txt"))
    s3.remove_object("/tmp/world.txt")

References
----------

#. `A local file cache for amazon S3 using python and
   boto <http://www.mccarroll.net/snippets/s3boto/index.html>`__

.. |Build Status| image:: https://travis-ci.org/vincetse/python-s3-cache.svg?branch=master
   :target: https://travis-ci.org/vincetse/python-s3-cache
   :alt: Build Status

.. |Code Coverage| image:: https://coveralls.io/repos/github/vincetse/python-s3-cache/badge.svg?branch=master
   :target: https://coveralls.io/github/vincetse/python-s3-cache?branch=master
   :alt: Code Coverage

.. |Code Climate| image:: https://codeclimate.com/github/vincetse/python-s3-cache/badges/issue_count.svg
   :target: https://codeclimate.com/github/vincetse/python-s3-cache
   :alt: Issue Count

