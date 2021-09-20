"""
Add transaction table
"""

from yoyo import step


__depends__ = {}

steps = [
    step(
        """CREATE TABLE IF NOT EXISTS exchange_rates(
            ts timestamp without time zone,
            from_currency varchar(3),
            to_currency varchar(3),
            rate numeric
         );""",
        """DROP TABLE IF EXISTS exchange_rates;""",
    )
]
