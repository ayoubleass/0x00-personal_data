#!/usr/bin/env python3
"""
This module uses regex in replacing occurrences of certain field values.
"""
import re
from typing import List
from os import getenv
import logging
import mysql.connector


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
        """
        Redact the fields in the log record message.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Redacts the specified fields in the message
    with the redacted value and separator.
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Return an instance of the connection object.
    """
    conn = mysql.connector.connection.MySQLConnection(
            user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=getenv('PERSONAL_DATA_DB_NAME')
        )
    return conn


def main():
    """
    Display each row under a filtered format.
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [field[0] for field in cursor.description]
    logger = get_logger()
    for row in cursor:
        record = dict(zip(field_names, row))
        message = ""
        for k, v in record.items():
            message += f'{k}={v}; '
        logger.info(message)
    cursor.close()
    db_conn.close()


if __name__ == "__main__":
    main()
