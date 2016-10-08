from classes.currency.exchange.exchangePairs import ExchangePairs
from multiprocessing import Pool

import requests
import settings

import logging

logger = logging.getLogger(__name__)


def load_exchange_pair(exchange_pair, api_json, process_id):
    ExchangePairs.load_exchange_pair_rates(exchange_pair, api_json, process_id)


class HttpWorker:
    def __init__(self):
        self.pool = None

    def init_new_pool(self):
        if not self.pool:
            self.pool = Pool()

    def close_pool(self):
        if self.pool is not None:
            self.pool.close()

    def init_new_worker(self, exchange_pair, worker_index):
        self.init_new_pool()

        api_json = self.load_url(exchange_pair["APIURL"]).text

        result = self.pool.apply_async(load_exchange_pair, (exchange_pair, api_json, worker_index))

        return result

    @staticmethod
    def load_url(url):
        r = requests.get(url, timeout=settings.REQUESTS_TIMEOUT, verify=False)

        if r.status_code != 200:
            logger.error("Error requesting " + str(url) + ", status code is not OK: " + str(r.status_code))

        return r
