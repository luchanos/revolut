import asyncio
import logging
import sys
from datetime import datetime

import asyncpg


logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")


class MyAsyncDbClient:
    TRANSACTION_INSERT_QUERY = """INSERT INTO transactions VALUES ($1, $2, $3, $4);"""
    EXCHANGE_RATES_INSERT_QUERY = """INSERT INTO exchange_rates VALUES ($1, $2, $3, $4)"""

    def __init__(self, db_url):
        self.db_url = db_url
        self.db_pool = None

    async def setup(self):
        logger.info("Db client had been set up!")
        self.db_pool = await asyncpg.create_pool(DB_URL)

    def _check_connection(self):
        if not self.db_pool:
            logger.warning("Pool has not been set up! Please, user client.setup method to create pool!")
            return False
        return True

    async def insert_new_transaction(self, date: str, user_id: int, currency: str, value: float):
        """Create new transaction"""
        self._check_connection()
        await self.db_pool.execute(
            self.TRANSACTION_INSERT_QUERY, datetime.strptime(date, "%Y-%m-%d %H:%M:%S"), user_id, currency, value
        )

    async def insert_new_exchange_rate(self, date: str, currency_1: str, currency_2: str, rate: float):
        """Create new exchange rate"""
        self._check_connection()
        await self.db_pool.execute(
            self.EXCHANGE_RATES_INSERT_QUERY,
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
            currency_1,
            currency_2,
            rate,
        )

    async def close(self):
        await self.db_pool.close()


exchange_rates_test_data = [
    ("2018-04-01 00:00:00", "USD", "GBP", "0.71"),
    ("2018-04-01 00:00:05", "USD", "GBP", "0.82"),
    ("2018-04-01 00:01:00", "USD", "GBP", "0.92"),
    ("2018-04-01 01:02:00", "USD", "GBP", "0.62"),
    ("2018-04-01 02:00:00", "USD", "GBP", "0.71"),
    ("2018-04-01 03:00:05", "USD", "GBP", "0.82"),
    ("2018-04-01 04:01:00", "USD", "GBP", "0.92"),
    ("2018-04-01 04:22:00", "USD", "GBP", "0.62"),
    ("2018-04-01 00:00:00", "EUR", "GBP", "1.71"),
    ("2018-04-01 01:00:05", "EUR", "GBP", "1.82"),
    ("2018-04-01 01:01:00", "EUR", "GBP", "1.92"),
    ("2018-04-01 01:02:00", "EUR", "GBP", "1.62"),
    ("2018-04-01 02:00:00", "EUR", "GBP", "1.71"),
    ("2018-04-01 03:00:05", "EUR", "GBP", "1.82"),
    ("2018-04-01 04:01:00", "EUR", "GBP", "1.92"),
    ("2018-04-01 05:22:00", "EUR", "GBP", "1.62"),
    ("2018-04-01 05:22:00", "EUR", "HUF", "0.062"),
]

transactions_test_data = [
    ("2018-04-01 00:00:00", 1, "EUR", 2.45),
    ("2018-04-01 01:00:00", 1, "EUR", 8.45),
    ("2018-04-01 01:30:00", 1, "USD", 3.5),
    ("2018-04-01 20:00:00", 1, "EUR", 2.45),
    ("2018-04-01 00:30:00", 2, "USD", 2.45),
    ("2018-04-01 01:20:00", 2, "USD", 0.45),
    ("2018-04-01 01:40:00", 2, "USD", 33.5),
    ("2018-04-01 18:00:00", 2, "EUR", 12.45),
    ("2018-04-01 18:01:00", 3, "GBP", 2),
    ("2018-04-01 00:01:00", 4, "USD", 2),
    ("2018-04-01 00:01:00", 4, "GBP", 2),
]


DB_URL = """postgresql://postgres:dbpass@localhost:5432/postgres"""


async def insert_test_data_to_db():
    my_shiny_db_client = MyAsyncDbClient(DB_URL)
    await my_shiny_db_client.setup()
    tasks_tr = [my_shiny_db_client.insert_new_transaction(*tr_info) for tr_info in transactions_test_data]
    tasks_ex = [my_shiny_db_client.insert_new_exchange_rate(*ex_info) for ex_info in exchange_rates_test_data]
    all_tasks = tasks_tr + tasks_ex
    await asyncio.gather(*all_tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_test_data_to_db())
