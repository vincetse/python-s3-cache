from setuptools import setup

setup(
    name='s3cache',
    version='0.1.0rc2',
    description='Local cache of S3 buckets',
    long_description=open('README.rst').read(),
    url='https://github.com/vincetse/python-s3-cache',
    author='Vince Tse, based on work by Niall McCarroll',
    author_email='thelazyenginerd@gmail.com',
    packages=['s3cache'],
    install_requires=[
        'boto',
    ],
    tests_require=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Filesystems',
    ],
    keywords=[
        'aws',
        's3',
        'cache',
    ]
)
