#!/bin/bash -eux

pep8
pylint s3cache
export S3_ENDPOINT=localhost S3_PORT=4569
nosetests -vs s3cache
