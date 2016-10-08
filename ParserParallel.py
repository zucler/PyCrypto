import logging
import time
import settings
import coloredlogs

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from classes.dbHelper import DbHelper
from classes.httpWorker import HttpWorker
from classes.currency.pairs import CurrencyPairs
from classes.currency.exchange.exchangePairs import ExchangePairs


def run_requests(exchange_pairs, http_workers):
    http_worker = HttpWorker()
    for exchange_pair in exchange_pairs:
        if exchange_pair in http_workers.keys():
            if http_workers[exchange_pair["ID"]].ready():
                http_worker.init_new_worker(exchange_pair, exchange_pairs.index(exchange_pair) + 1)
                # else:
                #   logger.debug("Still not finished: "+str(EXCHANGEPAIRS.index(ExPair)+1)+" : "+ ExPair[2])
        else:
            worker = http_worker.init_new_worker(exchange_pair, exchange_pairs.index(exchange_pair) + 1)
            http_workers[exchange_pair["ID"]] = worker

    http_worker.close_pool()
    time.sleep(2)

    return http_workers


# Init objects
logger = logging.getLogger('BookParses')

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

coloredlogs.install(level='DEBUG')

db = DbHelper(settings.DATABASE["USER"], settings.DATABASE["PASSWORD"], settings.DATABASE["HOST"],
              settings.DATABASE["PORT"], settings.DATABASE["SCHEMA"])

# Main workflow
currency_pairs_model = CurrencyPairs(db)
currency_pair = currency_pairs_model.get_by_id(settings.DEFAULT_CURRENCY_PAIR_ID)

exchange_pairs_model = ExchangePairs(db, currency_pair['ID'])
exchange_pairs = exchange_pairs_model.get_all()

logger.debug(currency_pair)
logger.debug(exchange_pairs)

db.close()

httpWorkers = {}
while True:
    httpWorkers = run_requests(exchange_pairs, httpWorkers)
