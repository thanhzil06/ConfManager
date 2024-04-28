import itertools as IT
from itertools import islice
from io import StringIO


class ErrorBeautifier:
    """
    This class will beautify error messages
    """

    def __init__(self, logger):
        self.logger = logger

    def beautify_lxml_parse_errors(self, err):
        line_err, column_err = err.position
        line = next(slice(StringIO(err), line_err))
        caret = '{:=>{}}'.format('^', column_err)
        err.msg = '{}\n{}\n{}'.format(err, line, caret)
        raise