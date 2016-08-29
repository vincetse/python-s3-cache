"""Utility functions"""
import os


def abspath(root, filepath):
    """Create a fully-qualified path from the temp root and filepath"""
    fullpath = "{0}{1}{2}".format(root, os.sep, filepath)
    dirname = os.path.abspath(fullpath)
    return dirname


def makedirs(filepath):
    """Ensure that the directories that the filepath exists,
    or creates them if they do not.
    """
    # joining paths, but using os.path.join() will given wrong output if
    # filepath looks like an absolute directory.
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
