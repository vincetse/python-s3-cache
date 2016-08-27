from setuptools import setup

setup(
    name='s3cache',
    version='0.0.0',
    description='S3 cache by Niall McCarroll, packaged by Vince Tse',
    long_description=open('README.md').read(),
    url='https://github.com/vincetse/python-s3-cache',
    license='MIT',
    author='Vince Tse',
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
)
