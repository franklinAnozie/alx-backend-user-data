#!/usr/bin/env python3
""" filtered logger file """

from typing import List
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format Fxn """
        new_record = filter_datum(self.fields, self.REDACTION,
                                  super().format(record), self.SEPARATOR)
        return new_record


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """ filter datus fxn """
    for field in fields:
        new_msg = f"{field}={redaction}{separator}"
        msg = re.sub(field + "=.*?" + field + redaction + separator, new_msg, message)
    return msg
