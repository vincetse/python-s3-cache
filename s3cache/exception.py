"""S3Cache exceptions."""


class S3CacheError(Exception):
    """S3cache exception base class"""

    def __init__(self, reason, *args):
        super(S3CacheError, self).__init__(reason, *args)
        self.reason = reason


class S3CacheConnectError(S3CacheError):
    """Cannot connect to endpoint"""

    def __init__(self, reason, *args):
        self.reason = "Cannot connect to S3 endpoint: {0}".format(reason)
        super(S3CacheConnectError, self).__init__(self.reason, *args)


class S3CacheBucketNotExistError(S3CacheError):
    """Operating on a non-existent bucket"""

    def __init__(self, reason, *args):
        self.reason = "Bucket does not exist: {0}".format(reason)
        super(S3CacheBucketNotExistError, self).__init__(self.reason, *args)


class S3CacheIOError(S3CacheError):
    """Error opening file"""

    def __init__(self, reason, *args):
        self.reason = "Error opening file: {0}".format(reason)
        super(S3CacheIOError, self).__init__(self.reason, *args)
